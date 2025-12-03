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
from django.db.models import Sum, Q, Count

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
        from chamas.models import Member, Transaction, ChamaGroup
        from decimal import Decimal
        
        user = request.user
        
        # Get the Chama group
        chama_group = ChamaGroup.objects.first()
        
        # For members
        if not user.is_staff:
            # Get member data
            try:
                member = Member.objects.get(user=user)
            except Member.DoesNotExist:
                return Response({
                    'error': 'Member profile not found. Please contact the administrator.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Calculate personal balance
            personal_balance = float(member.calculate_net_balance())
            
            # Get group balance
            group_balance = float(chama_group.calculate_total_balance()) if chama_group else 0
            
            # Get current month stats
            now = timezone.now()
            current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # Calculate contribution summary
            contributions = Transaction.objects.filter(
                member=member,
                transaction_type='CONTRIBUTION',
                status='VERIFIED'
            )
            
            this_month_contributions = contributions.filter(
                date__gte=current_month_start
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            
            total_contributions = contributions.aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0.00')
            
            last_contribution = contributions.order_by('-date').first()
            
            # Get loan status (if member has any payouts)
            payouts = Transaction.objects.filter(
                member=member,
                transaction_type='PAYOUT',
                status='VERIFIED'
            )
            
            loan_status = None
            if payouts.exists():
                total_borrowed = payouts.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
                # For simplicity, assume 50% has been paid (in real app, track repayments)
                amount_paid = total_borrowed * Decimal('0.5')
                remaining_balance = total_borrowed - amount_paid
                
                loan_status = {
                    'active': True,
                    'amount_borrowed': float(total_borrowed),
                    'amount_paid': float(amount_paid),
                    'remaining_balance': float(remaining_balance),
                    'next_payment_date': (now + timedelta(days=30)).isoformat(),
                    'next_payment_amount': 5000,
                }
            
            # Get recent transactions
            recent_txns = Transaction.objects.filter(
                member=member,
                status='VERIFIED'
            ).order_by('-date')[:5]
            
            recent_transactions = []
            for txn in recent_txns:
                txn_type_map = {
                    'CONTRIBUTION': 'contribution',
                    'FINE': 'fine',
                    'PAYOUT': 'loan_disbursement',
                    'EXPENSE': 'expense',
                }
                recent_transactions.append({
                    'id': str(txn.id),
                    'date': txn.date.isoformat(),
                    'type': txn_type_map.get(txn.transaction_type, 'contribution'),
                    'amount': float(txn.amount),
                    'description': txn.description or f'{txn.get_transaction_type_display()}',
                    'status': 'completed',
                })
            
            data = {
                'personal_balance': personal_balance,
                'group_balance': group_balance,
                'next_meeting': {
                    'date': (now + timedelta(days=7)).isoformat(),
                    'time': '14:00',
                    'location': 'Community Hall, Nairobi',
                    'agenda': 'Monthly contributions and loan approvals',
                    'my_position': 3,
                    'total_positions': Member.objects.filter(status='ACTIVE').count(),
                },
                'loan_status': loan_status,
                'recent_transactions': recent_transactions,
                'contribution_summary': {
                    'this_month': float(this_month_contributions),
                    'total': float(total_contributions),
                    'last_contribution_date': last_contribution.date.isoformat() if last_contribution else None,
                },
            }
        # For treasurers/staff
        else:
            now = timezone.now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # Get group balance
            total_balance = float(chama_group.calculate_total_balance()) if chama_group else 0
            
            # Get today's collections
            total_collected_today = Transaction.objects.filter(
                transaction_type='CONTRIBUTION',
                status='VERIFIED',
                date__gte=today_start
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            
            # Get outstanding loans (total payouts - we'd track repayments in real app)
            outstanding_loans = Transaction.objects.filter(
                transaction_type='PAYOUT',
                status='VERIFIED'
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            
            # Get total members
            total_members = Member.objects.filter(status='ACTIVE').count()
            
            # Find defaulters (members with fines or who haven't contributed this month)
            members_with_fines_ids = Member.objects.filter(
                transactions__transaction_type='FINE',
                transactions__status='VERIFIED'
            ).values_list('id', flat=True).distinct()
            
            members_without_contribution_ids = Member.objects.filter(
                status='ACTIVE'
            ).exclude(
                transactions__transaction_type='CONTRIBUTION',
                transactions__status='VERIFIED',
                transactions__date__gte=current_month_start
            ).values_list('id', flat=True)
            
            # Combine member IDs
            defaulter_ids = set(members_with_fines_ids) | set(members_without_contribution_ids)
            defaulters_queryset = Member.objects.filter(id__in=list(defaulter_ids))[:5]
            
            defaulters_list = []
            for member in defaulters_queryset:
                fines = Transaction.objects.filter(
                    member=member,
                    transaction_type='FINE',
                    status='VERIFIED'
                ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
                
                last_contribution = Transaction.objects.filter(
                    member=member,
                    transaction_type='CONTRIBUTION',
                    status='VERIFIED'
                ).order_by('-date').first()
                
                days_overdue = 0
                if last_contribution:
                    days_overdue = (now - last_contribution.date).days
                else:
                    days_overdue = 90  # No contributions ever
                
                defaulters_list.append({
                    'id': str(member.id),
                    'name': member.name,
                    'phone': member.phone_number,
                    'amount': float(fines),
                    'days_overdue': days_overdue,
                    'last_contribution': last_contribution.date.isoformat() if last_contribution else None,
                })
            
            # Get pending transactions count
            pending_transactions = Transaction.objects.filter(status='PENDING').count()
            
            # Get recent group transactions
            recent_group_txns = Transaction.objects.filter(
                status='VERIFIED'
            ).order_by('-date')[:10]
            
            recent_group_transactions = []
            for txn in recent_group_txns:
                txn_type_map = {
                    'CONTRIBUTION': 'contribution',
                    'FINE': 'fine',
                    'PAYOUT': 'loan_payment',
                    'EXPENSE': 'expense',
                }
                recent_group_transactions.append({
                    'id': str(txn.id),
                    'date': txn.date.isoformat(),
                    'type': txn_type_map.get(txn.transaction_type, 'contribution'),
                    'member_name': txn.member.name if txn.member else 'Group',
                    'amount': float(txn.amount),
                    'description': txn.description or f'{txn.get_transaction_type_display()}',
                    'status': 'completed',
                })
            
            data = {
                'group_summary': {
                    'total_balance': total_balance,
                    'total_collected_today': float(total_collected_today),
                    'outstanding_loans': float(outstanding_loans),
                    'defaulters_count': len(defaulters_list),
                    'total_members': total_members,
                    'attendance_rate': 85,  # Would be calculated from meeting attendance in real app
                },
                'defaulters': defaulters_list,
                'pending_actions': {
                    'pending_loans': 0,  # Would track loan applications
                    'pending_approvals': pending_transactions,
                    'upcoming_meetings': 1,
                    'overdue_fines': len(defaulters_list),
                },
                'recent_group_transactions': recent_group_transactions,
            }
        
        return Response(data, status=status.HTTP_200_OK)
