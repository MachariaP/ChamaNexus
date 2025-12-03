from rest_framework import serializers
from .models import Member, Transaction, ChamaGroup


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for Member model"""
    net_balance = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = [
            'id', 'name', 'phone_number', 'role', 'status',
            'net_balance', 'payment_status', 'is_admin',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_net_balance(self, obj):
        """Get member's net balance"""
        return float(obj.calculate_net_balance())
    
    def get_payment_status(self, obj):
        """Get payment status for current cycle"""
        # Get expected amount from context if available
        request = self.context.get('request')
        expected_amount = None
        
        if request and hasattr(request, 'chama_group'):
            expected_amount = request.chama_group.monthly_contribution_amount
        
        return obj.get_payment_status(expected_amount)
    
    def get_is_admin(self, obj):
        """Check if member has admin privileges"""
        return obj.is_admin_or_treasurer()


class MemberListSerializer(serializers.ModelSerializer):
    """Simplified serializer for member lists"""
    
    class Meta:
        model = Member
        fields = ['id', 'name', 'phone_number', 'role', 'status']
        read_only_fields = ['id']


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction model.
    
    Part 3: Required UI/User Flow (Treasurer)
    Supports the data entry step: select member, amount, M-Pesa code
    """
    member_name = serializers.CharField(source='member.name', read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'member', 'member_name', 'amount', 'date',
            'transaction_type', 'transaction_type_display',
            'mpesa_code', 'status', 'status_display',
            'description', 'created_by', 'created_by_email',
            'verified_by', 'verified_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 
            'verified_by', 'verified_at', 'created_by'
        ]
    
    def validate_mpesa_code(self, value):
        """
        Business Logic Rule 1: Validate M-Pesa code uniqueness
        Ensure no duplicate transactions are logged
        """
        value = value.upper().strip()
        
        # Check if updating existing transaction
        instance = self.instance
        
        # Check for duplicates
        duplicate = Transaction.objects.filter(mpesa_code=value)
        if instance:
            duplicate = duplicate.exclude(pk=instance.pk)
        
        if duplicate.exists():
            raise serializers.ValidationError(
                "This M-Pesa transaction code has already been logged. "
                "Duplicate contributions are not allowed."
            )
        
        return value
    
    def validate(self, data):
        """Additional validation"""
        # Ensure member is provided for non-expense transactions
        transaction_type = data.get('transaction_type')
        member = data.get('member')
        
        if transaction_type != 'EXPENSE' and not member:
            raise serializers.ValidationError({
                'member': f'{transaction_type} transactions must be linked to a member.'
            })
        
        return data


class TransactionCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating transactions.
    
    Part 3: Step 2 - Data Entry (select member, amount, M-Pesa code)
    """
    
    class Meta:
        model = Transaction
        fields = ['member', 'amount', 'mpesa_code', 'transaction_type', 'date', 'description']
    
    def validate_mpesa_code(self, value):
        """Business Logic Rule 1: Check for duplicate M-Pesa codes"""
        value = value.upper().strip()
        
        if Transaction.objects.filter(mpesa_code=value).exists():
            raise serializers.ValidationError(
                "This M-Pesa code has already been used. Duplicate contributions are not allowed."
            )
        
        return value
    
    def create(self, validated_data):
        """
        Part 3: Step 3 - System Action (verification check and saving)
        """
        # Set created_by from request context
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        
        # Create transaction with PENDING status by default
        validated_data['status'] = 'PENDING'
        
        return super().create(validated_data)


class ChamaGroupSerializer(serializers.ModelSerializer):
    """Serializer for ChamaGroup model"""
    total_balance = serializers.SerializerMethodField()
    total_fines = serializers.SerializerMethodField()
    
    class Meta:
        model = ChamaGroup
        fields = [
            'id', 'name', 'description', 
            'monthly_contribution_amount',
            'total_balance', 'total_fines',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_balance(self, obj):
        """Business Logic Rule 3: Get group's total balance"""
        return float(obj.calculate_total_balance())
    
    def get_total_fines(self, obj):
        """Get total fines collected"""
        return float(obj.get_total_fines())
