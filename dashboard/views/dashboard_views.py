"""
Dashboard view sets for ChamaNexus API.
"""

from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.utils import timezone
from datetime import timedelta

from dashboard.serializers import (
    MemberDashboardSerializer,
    TreasurerDashboardSerializer,
    DashboardSummarySerializer,
)


class DashboardViewSet(GenericViewSet):
    """Dashboard endpoints for both members and treasurers"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'], url_path='summary')
    def dashboard_summary(self, request):
        """Get dashboard summary for authenticated user"""
        user = request.user
        
        # This is mock data - replace with actual database queries when models are ready
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
                } if user.id.int % 3 == 0 else None,  # Only some users have loans
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
            serializer = MemberDashboardSerializer(data)
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
            serializer = TreasurerDashboardSerializer(data)
        
        return Response(data, status=status.HTTP_200_OK)
