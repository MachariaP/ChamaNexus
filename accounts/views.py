from django.conf import settings
from rest_framework import status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import User
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserProfileSerializer, ChangePasswordSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
import uuid
from datetime import timedelta

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

            # Send welcome email (in production)
            if not settings.DEBUG:
                try:
                    from .emails import send_welcome_email
                    send_welcome_email(user.email, user.first_name)
                except ImportError:
                    pass
            
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
            
            # Login for session auth (helps with CSRF)
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
                'message': 'Logout successful',
                'redirect_url': settings.FRONTEND_URL
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'User not authenticated',
            'redirect_url': settings.FRONTEND_URL
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
            
            # Update token (force re-login)
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
                
                # Generate reset token
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
            'timestamp': timezone.now().isoformat(),
            'debug': settings.DEBUG,
            'api_version': 'v1'
        })

class DashboardViewSet(GenericViewSet):
    """Dashboard endpoints"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'], url_path='summary')
    def dashboard_summary(self, request):
        """Get dashboard summary for authenticated user"""
        user = request.user
        
        # This is mock data - replace with actual database queries
        # For members
        if not user.is_staff:
            data = {
                'personal_balance': 125000,
                'group_balance': 2450000,
                'next_meeting': {
                    'date': (timezone.now() + timedelta(days=7)).isoformat(),
                    'time': '14:00',
                    'location': 'Community Hall, Nairobi',
                    'agenda': 'Monthly contributions and loan approvals',
                    'my_position': 3,
                    'total_positions': 15,
                },
                'loan_status': {
                    'active': True,
                    'amount_borrowed': 50000,
                    'amount_paid': 25000,
                    'remaining_balance': 25000,
                    'next_payment_date': (timezone.now() + timedelta(days=14)).isoformat(),
                    'next_payment_amount': 5000,
                } if user.id % 3 == 0 else None,  # Only some users have loans
                'recent_transactions': [
                    {
                        'id': '1',
                        'date': (timezone.now() - timedelta(days=2)).isoformat(),
                        'type': 'contribution',
                        'amount': 5000,
                        'description': 'Monthly contribution',
                        'status': 'completed',
                    },
                    {
                        'id': '2',
                        'date': (timezone.now() - timedelta(days=30)).isoformat(),
                        'type': 'loan_payment',
                        'amount': 5000,
                        'description': 'Loan installment',
                        'status': 'completed',
                    },
                    {
                        'id': '3',
                        'date': (timezone.now() - timedelta(days=60)).isoformat(),
                        'type': 'loan_disbursement',
                        'amount': 50000,
                        'description': 'Business loan',
                        'status': 'completed',
                    },
                ],
                'contribution_summary': {
                    'this_month': 5000,
                    'total': 125000,
                    'last_contribution_date': (timezone.now() - timedelta(days=2)).isoformat(),
                },
            }
        # For treasurers/staff
        else:
            data = {
                'group_summary': {
                    'total_balance': 2450000,
                    'total_collected_today': 75000,
                    'outstanding_loans': 450000,
                    'defaulters_count': 3,
                    'total_members': 25,
                    'attendance_rate': 88,
                },
                'defaulters': [
                    {
                        'id': '1',
                        'name': 'John Kamau',
                        'phone': '0712345678',
                        'amount': 10000,
                        'days_overdue': 45,
                        'last_contribution': (timezone.now() - timedelta(days=60)).isoformat(),
                    },
                    {
                        'id': '2',
                        'name': 'Mary Wanjiku',
                        'phone': '0723456789',
                        'amount': 5000,
                        'days_overdue': 30,
                        'last_contribution': (timezone.now() - timedelta(days=45)).isoformat(),
                    },
                    {
                        'id': '3',
                        'name': 'Peter Otieno',
                        'phone': '0734567890',
                        'amount': 15000,
                        'days_overdue': 15,
                        'last_contribution': (timezone.now() - timedelta(days=30)).isoformat(),
                    },
                ],
                'pending_actions': {
                    'pending_loans': 5,
                    'pending_approvals': 3,
                    'upcoming_meetings': 1,
                    'overdue_fines': 2,
                },
                'recent_group_transactions': [
                    {
                        'id': '1',
                        'date': (timezone.now() - timedelta(hours=2)).isoformat(),
                        'type': 'contribution',
                        'member_name': 'Jane Muthoni',
                        'amount': 5000,
                        'description': 'Monthly contribution',
                        'status': 'completed',
                    },
                    {
                        'id': '2',
                        'date': (timezone.now() - timedelta(days=1)).isoformat(),
                        'type': 'loan_payment',
                        'member_name': 'David Kiprop',
                        'amount': 10000,
                        'description': 'Loan repayment',
                        'status': 'completed',
                    },
                    {
                        'id': '3',
                        'date': (timezone.now() - timedelta(days=2)).isoformat(),
                        'type': 'contribution',
                        'member_name': 'Grace Akinyi',
                        'amount': 5000,
                        'description': 'Monthly contribution',
                        'status': 'completed',
                    },
                ],
            }
        
        return Response(data, status=status.HTTP_200_OK)
