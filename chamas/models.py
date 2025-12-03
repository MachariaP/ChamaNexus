import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum, Q
from django.utils import timezone
from decimal import Decimal


class Member(models.Model):
    """
    Represents a person in the Chama (Savings Group).
    
    Part 1: Core Data Model - Member
    Fields: Name, Phone Number, Chama Role/Permission, Status
    """
    
    # Role choices for Chama members
    ROLE_CHOICES = [
        ('TREASURER', 'Treasurer'),
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # User link (optional - can be linked to system user or standalone)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='memberships'
    )
    
    # Core fields as per requirements
    name = models.CharField(
        max_length=255,
        help_text="Full name of the member"
    )
    
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?254\d{9}$|^0\d{9}$',
                message='Enter a valid Kenyan phone number (e.g., +254712345678 or 0712345678)'
            )
        ],
        help_text="Kenyan phone number for M-Pesa transactions"
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='MEMBER',
        help_text="Chama role/permission level"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        help_text="Current membership status"
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chama_members'
        verbose_name = 'Chama Member'
        verbose_name_plural = 'Chama Members'
        ordering = ['name']
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['status']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"
    
    def clean(self):
        """Custom validation"""
        super().clean()
        
        # Normalize phone number to Kenyan format
        if self.phone_number:
            phone = self.phone_number.strip()
            # Convert 07XX to +2547XX format
            if phone.startswith('0'):
                phone = '+254' + phone[1:]
            self.phone_number = phone
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    # Business Logic Rule 4: Admin Access Logic
    def is_admin_or_treasurer(self):
        """Check if member has admin/treasurer privileges"""
        return self.role in ['TREASURER', 'ADMIN']
    
    # Business Logic Rule 2: Member Statement Logic
    def calculate_net_balance(self):
        """
        Calculate member's net balance.
        Formula: Total Contributions - (Fines + Payouts)
        """
        contributions = self.transactions.filter(
            transaction_type='CONTRIBUTION',
            status='VERIFIED'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        fines = self.transactions.filter(
            transaction_type='FINE',
            status='VERIFIED'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        payouts = self.transactions.filter(
            transaction_type='PAYOUT',
            status='VERIFIED'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        return contributions - (fines + payouts)
    
    # Business Logic Rule 5: Payment Status Logic
    def get_payment_status(self, expected_amount=None):
        """
        Determine if member is 'Paid', 'Short', or 'Overdue' for current cycle.
        
        Args:
            expected_amount: Expected contribution amount for the cycle
            
        Returns:
            str: 'PAID', 'SHORT', or 'OVERDUE'
        """
        if not expected_amount:
            # If no expected amount set, can't determine status
            return 'UNKNOWN'
        
        # Get current month's contributions
        now = timezone.now()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        monthly_contributions = self.transactions.filter(
            transaction_type='CONTRIBUTION',
            status='VERIFIED',
            date__gte=current_month_start
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        if monthly_contributions >= expected_amount:
            return 'PAID'
        elif monthly_contributions > 0:
            return 'SHORT'
        else:
            # Check if payment is overdue (e.g., past 7th day of month)
            if now.day > 7:
                return 'OVERDUE'
            return 'SHORT'


class Transaction(models.Model):
    """
    Represents a contribution, fine, or group expense.
    
    Part 1: Core Data Model - Transaction
    Fields: Amount, Date, Transaction Type, Link to Member, M-Pesa Code (Verification Detail)
    """
    
    # Transaction type choices
    TYPE_CHOICES = [
        ('CONTRIBUTION', 'Contribution'),
        ('FINE', 'Fine'),
        ('PAYOUT', 'Payout'),
        ('EXPENSE', 'Group Expense'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('PENDING', 'Pending Verification'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Link to Member (required for contributions, fines, payouts)
    member = models.ForeignKey(
        Member,
        on_delete=models.PROTECT,
        related_name='transactions',
        null=True,
        blank=True,
        help_text="Member associated with this transaction (not required for group expenses)"
    )
    
    # Core transaction fields
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Transaction amount in KES"
    )
    
    date = models.DateTimeField(
        default=timezone.now,
        help_text="Date and time of transaction"
    )
    
    transaction_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        help_text="Type of transaction"
    )
    
    # Business Logic Rule 1: Data Integrity Logic
    # M-Pesa transaction code serves as unique identifier to prevent duplicates
    mpesa_code = models.CharField(
        max_length=20,
        unique=True,
        help_text="M-Pesa transaction code (unique identifier)",
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9]{10}$',
                message='Enter a valid M-Pesa code (10 alphanumeric characters)'
            )
        ]
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        help_text="Verification status"
    )
    
    # Additional fields
    description = models.TextField(
        blank=True,
        help_text="Optional description or notes"
    )
    
    # Audit fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_transactions',
        help_text="User who created this transaction (typically Treasurer)"
    )
    
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_transactions',
        help_text="User who verified this transaction"
    )
    
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the transaction was verified"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chama_transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['mpesa_code']),
            models.Index(fields=['transaction_type', 'status']),
            models.Index(fields=['date']),
            models.Index(fields=['member', 'date']),
        ]
    
    def __str__(self):
        member_name = self.member.name if self.member else "Group"
        return f"{self.get_transaction_type_display()} - {member_name} - KES {self.amount} ({self.mpesa_code})"
    
    def clean(self):
        """Custom validation"""
        super().clean()
        
        # Business Logic Rule 1: Ensure M-Pesa code uniqueness
        if self.mpesa_code:
            self.mpesa_code = self.mpesa_code.upper().strip()
            
            # Check for duplicate M-Pesa codes
            duplicate = Transaction.objects.filter(
                mpesa_code=self.mpesa_code
            ).exclude(pk=self.pk).exists()
            
            if duplicate:
                raise ValidationError({
                    'mpesa_code': 'This M-Pesa transaction code has already been logged. Duplicate contributions are not allowed.'
                })
        
        # Validate that member is required for non-expense transactions
        if self.transaction_type != 'EXPENSE' and not self.member:
            raise ValidationError({
                'member': f'{self.get_transaction_type_display()} transactions must be linked to a member.'
            })
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def verify(self, verified_by_user):
        """
        Verify the transaction.
        
        Business Logic Rule 4: Only admin/treasurer can verify transactions
        """
        self.status = 'VERIFIED'
        self.verified_by = verified_by_user
        self.verified_at = timezone.now()
        self.save()
    
    def reject(self, verified_by_user):
        """Reject the transaction"""
        self.status = 'REJECTED'
        self.verified_by = verified_by_user
        self.verified_at = timezone.now()
        self.save()


# Business Logic Rule 3: Group Balance Logic
class ChamaGroup(models.Model):
    """
    Represents the Chama group itself for aggregate calculations.
    This is optional but useful for tracking group-level settings and balances.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Contribution settings
    monthly_contribution_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Expected monthly contribution per member in KES"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chama_groups'
        verbose_name = 'Chama Group'
        verbose_name_plural = 'Chama Groups'
    
    def __str__(self):
        return self.name
    
    def calculate_total_balance(self):
        """
        Business Logic Rule 3: Calculate Chama's total cash assets.
        Formula: Sum of all verified contributions + fines - (Sum of all payouts + Sum of all expenses)
        Note: Fines add to the group balance as they represent additional income
        """
        contributions = Transaction.objects.filter(
            transaction_type='CONTRIBUTION',
            status='VERIFIED'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        fines = Transaction.objects.filter(
            transaction_type='FINE',
            status='VERIFIED'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        payouts = Transaction.objects.filter(
            transaction_type='PAYOUT',
            status='VERIFIED'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        expenses = Transaction.objects.filter(
            transaction_type='EXPENSE',
            status='VERIFIED'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        return contributions + fines - (payouts + expenses)
    
    def get_total_fines(self):
        """Get total fines collected (these stay in the group)"""
        return Transaction.objects.filter(
            transaction_type='FINE',
            status='VERIFIED'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
