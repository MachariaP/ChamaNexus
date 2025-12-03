from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Member, Transaction, ChamaGroup
from .serializers import (
    MemberSerializer, MemberListSerializer,
    TransactionSerializer, TransactionCreateSerializer,
    ChamaGroupSerializer
)
from .permissions import IsTreasurerOrAdmin


class MemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Chama members.
    
    List, create, retrieve, update, and delete members.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Use simplified serializer for list view"""
        if self.action == 'list':
            return MemberListSerializer
        return MemberSerializer
    
    @action(detail=True, methods=['get'])
    def statement(self, request, pk=None):
        """
        Business Logic Rule 2: Get member's statement.
        Returns net balance and transaction history.
        """
        member = self.get_object()
        
        # Get all transactions for this member
        transactions = member.transactions.filter(status='VERIFIED').order_by('-date')
        
        data = {
            'member': MemberSerializer(member).data,
            'net_balance': float(member.calculate_net_balance()),
            'transactions': TransactionSerializer(transactions, many=True).data
        }
        
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def payment_status(self, request, pk=None):
        """
        Business Logic Rule 5: Get member's payment status.
        """
        member = self.get_object()
        
        # Get expected contribution amount
        try:
            chama_group = ChamaGroup.objects.first()
            expected_amount = chama_group.monthly_contribution_amount if chama_group else None
        except ChamaGroup.DoesNotExist:
            expected_amount = None
        
        status_value = member.get_payment_status(expected_amount)
        
        return Response({
            'member': member.name,
            'payment_status': status_value,
            'expected_amount': float(expected_amount) if expected_amount else None,
            'net_balance': float(member.calculate_net_balance())
        })


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing transactions.
    
    Part 3: Required UI/User Flow (Treasurer)
    This implements the complete flow for logging contributions.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Use create serializer for POST requests"""
        if self.action == 'create':
            return TransactionCreateSerializer
        return TransactionSerializer
    
    def get_permissions(self):
        """
        Business Logic Rule 4: Admin Access Logic
        Only Treasurer/Admin can create, update, or delete transactions
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'verify', 'reject']:
            permission_classes = [permissions.IsAuthenticated, IsTreasurerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """
        Part 3: Complete Treasurer Flow
        
        Step 1: Accessing the logging screen (handled by frontend routing to this endpoint)
        Step 2: Data entry (member, amount, M-Pesa code received in request)
        Step 3: System action (verification check and saving)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save transaction
        transaction = serializer.save()
        
        # Return created transaction with full details
        response_serializer = TransactionSerializer(transaction)
        
        return Response(
            {
                'message': 'Transaction logged successfully. Pending verification.',
                'transaction': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify a transaction.
        Business Logic Rule 4: Only admin/treasurer can verify
        """
        transaction = self.get_object()
        
        if transaction.status == 'VERIFIED':
            return Response(
                {'error': 'Transaction is already verified.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.verify(request.user)
        
        return Response({
            'message': 'Transaction verified successfully.',
            'transaction': TransactionSerializer(transaction).data
        })
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Reject a transaction.
        Business Logic Rule 4: Only admin/treasurer can reject
        """
        transaction = self.get_object()
        
        if transaction.status == 'REJECTED':
            return Response(
                {'error': 'Transaction is already rejected.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.reject(request.user)
        
        return Response({
            'message': 'Transaction rejected.',
            'transaction': TransactionSerializer(transaction).data
        })
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending transactions for verification"""
        pending_transactions = self.queryset.filter(status='PENDING')
        serializer = self.get_serializer(pending_transactions, many=True)
        return Response(serializer.data)


class ChamaGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Chama group settings.
    """
    queryset = ChamaGroup.objects.all()
    serializer_class = ChamaGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """Only admin/treasurer can modify group settings"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsTreasurerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def balance(self, request, pk=None):
        """
        Business Logic Rule 3: Get Chama's total balance.
        """
        group = self.get_object()
        
        return Response({
            'group_name': group.name,
            'total_balance': float(group.calculate_total_balance()),
            'total_fines': float(group.get_total_fines()),
            'monthly_contribution_amount': float(group.monthly_contribution_amount)
        })
