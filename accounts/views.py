from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserProfileSerializer, ChangePasswordSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from .emails import send_welcome_email
import uuid

class AuthViewSet(GenericViewSet):
    """Authentication endpoints"""
    
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """User registration endpoint"""
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Create auth token
            token, created = Token.objects.get_or_create(user=user)

            # Send welcome email
            if not settings.DEBUG:
                send_welcome_message(user.email, user.first_name)
            
            # Prepare response data
            user_data = UserSerializer(user, context={'request': request}).data
            
            return Response({
                'message': 'User registered successfully',
                'user': user_data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """User login endpoint"""
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Create or get auth token
            token, created = Token.objects.get_or_create(user=user)
            
            # Optional: Login for session auth (if using sessions)
            login(request, user)
            
            user_data = UserSerializer(user, context={'request': request}).data
            
            return Response({
                'message': 'Login successful',
                'user': user_data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        """User logout endpoint"""
        if request.user.is_authenticated:
            # Delete token if using token authentication
            try:
                Token.objects.filter(user=request.user).delete()
            except Token.DoesNotExist:
                pass
            
            # Logout for session auth
            logout(request)
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'User not authenticated'
        }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """User profile management"""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

    @action(detail=False, methods=['get', 'put'], url_path='profile')
    def profile(self, request):
        """Get or update user profile"""
        if request.method == 'GET':
            serializer = UserSerializer(request.user, context={'request': request})
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = UserSerializer(
                request.user, 
                data=request.data, 
                partial=True,
                context={'request': request}
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], url_path='change-password')
    def change_password(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.last_password_change = timezone.now()
            user.save()
            
            # Update token (optional: force re-login)
            Token.objects.filter(user=user).delete()
            new_token = Token.objects.create(user=user)
            
            return Response({
                'message': 'Password changed successfully',
                'token': new_token.key
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    """Password reset functionality"""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Request password reset"""
        serializer = PasswordResetRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email, is_active=True)
                
                # Generate reset token (in production, send email)
                reset_token = str(uuid.uuid4())
                user.verification_token = reset_token
                user.verification_sent_at = timezone.now()
                user.save()
                
                # In production: Send email with reset link
                # reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
                # send_password_reset_email(user.email, reset_link)
                
                return Response({
                    'message': 'Password reset instructions sent to your email',
                    'reset_token': reset_token  # Remove in production
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                # Don't reveal whether email exists
                return Response({
                    'message': 'If the email exists, reset instructions have been sent'
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    """Confirm password reset"""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Confirm password reset with token"""
        reset_token = request.data.get('reset_token')
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if not reset_token:
            return Response({
                'error': 'Reset token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            try:
                user = User.objects.get(
                    verification_token=reset_token,
                    is_active=True
                )
                
                # Check if token is expired (24 hours)
                if (user.verification_sent_at and 
                    (timezone.now() - user.verification_sent_at).total_seconds() > 86400):
                    return Response({
                        'error': 'Reset token has expired'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Update password
                user.set_password(serializer.validated_data['new_password'])
                user.last_password_change = timezone.now()
                user.verification_token = None
                user.verification_sent_at = None
                user.reset_failed_logins()  # Reset any login locks
                user.save()
                
                # Delete existing tokens
                Token.objects.filter(user=user).delete()
                
                return Response({
                    'message': 'Password reset successfully'
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                return Response({
                    'error': 'Invalid or expired reset token'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HealthCheckView(APIView):
    """API health check"""
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'service': 'ChamaNexus API',
            'timestamp': timezone.now().isoformat()
        })
