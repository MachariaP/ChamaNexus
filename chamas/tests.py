from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Member, Transaction, ChamaGroup

User = get_user_model()


class MemberModelTest(TestCase):
    """Tests for the Member model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='treasurer@example.com',
            password='testpass123',
            first_name='John',
            last_name='Treasurer'
        )
        
        self.member = Member.objects.create(
            name='Jane Doe',
            phone_number='+254712345678',
            role='MEMBER',
            status='ACTIVE'
        )
        
        self.treasurer = Member.objects.create(
            name='John Treasurer',
            phone_number='+254722334455',
            role='TREASURER',
            status='ACTIVE',
            user=self.user
        )
    
    def test_member_creation(self):
        """Test creating a member"""
        self.assertEqual(self.member.name, 'Jane Doe')
        self.assertEqual(self.member.role, 'MEMBER')
        self.assertEqual(self.member.status, 'ACTIVE')
    
    def test_phone_number_normalization(self):
        """Test phone number is normalized to +254 format"""
        member = Member.objects.create(
            name='Test User',
            phone_number='0712345678',
            role='MEMBER'
        )
        self.assertEqual(member.phone_number, '+254712345678')
    
    def test_is_admin_or_treasurer(self):
        """Test Business Logic Rule 4: Admin Access Logic"""
        self.assertTrue(self.treasurer.is_admin_or_treasurer())
        self.assertFalse(self.member.is_admin_or_treasurer())
    
    def test_calculate_net_balance_empty(self):
        """Test Business Logic Rule 2: Member Statement Logic - no transactions"""
        balance = self.member.calculate_net_balance()
        self.assertEqual(balance, Decimal('0.00'))
    
    def test_calculate_net_balance_with_transactions(self):
        """Test Business Logic Rule 2: Member Statement Logic - with transactions"""
        # Create verified contribution
        Transaction.objects.create(
            member=self.member,
            amount=Decimal('1000.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='ABC1234567',
            status='VERIFIED'
        )
        
        # Create verified fine
        Transaction.objects.create(
            member=self.member,
            amount=Decimal('100.00'),
            transaction_type='FINE',
            mpesa_code='DEF1234567',
            status='VERIFIED'
        )
        
        balance = self.member.calculate_net_balance()
        self.assertEqual(balance, Decimal('900.00'))  # 1000 - 100
    
    def test_get_payment_status_paid(self):
        """Test Business Logic Rule 5: Payment Status - PAID"""
        # Create this month's contribution
        Transaction.objects.create(
            member=self.member,
            amount=Decimal('1000.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='XYZ1234567',
            status='VERIFIED',
            date=timezone.now()
        )
        
        status = self.member.get_payment_status(expected_amount=Decimal('1000.00'))
        self.assertEqual(status, 'PAID')
    
    def test_get_payment_status_short(self):
        """Test Business Logic Rule 5: Payment Status - SHORT"""
        # Create partial contribution
        Transaction.objects.create(
            member=self.member,
            amount=Decimal('500.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='XYZ1234567',
            status='VERIFIED',
            date=timezone.now()
        )
        
        status = self.member.get_payment_status(expected_amount=Decimal('1000.00'))
        self.assertEqual(status, 'SHORT')


class TransactionModelTest(TestCase):
    """Tests for the Transaction model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='treasurer@example.com',
            password='testpass123',
            first_name='John',
            last_name='Treasurer'
        )
        
        self.member = Member.objects.create(
            name='Jane Doe',
            phone_number='+254712345678',
            role='MEMBER',
            status='ACTIVE'
        )
    
    def test_transaction_creation(self):
        """Test creating a transaction"""
        transaction = Transaction.objects.create(
            member=self.member,
            amount=Decimal('1000.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='ABC1234567',
            created_by=self.user
        )
        
        self.assertEqual(transaction.amount, Decimal('1000.00'))
        self.assertEqual(transaction.status, 'PENDING')
        self.assertEqual(transaction.mpesa_code, 'ABC1234567')
    
    def test_duplicate_mpesa_code_validation(self):
        """Test Business Logic Rule 1: Data Integrity - duplicate M-Pesa codes not allowed"""
        # Create first transaction
        Transaction.objects.create(
            member=self.member,
            amount=Decimal('1000.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='ABC1234567'
        )
        
        # Try to create duplicate - should raise ValidationError
        with self.assertRaises(ValidationError):
            transaction2 = Transaction(
                member=self.member,
                amount=Decimal('1000.00'),
                transaction_type='CONTRIBUTION',
                mpesa_code='ABC1234567'
            )
            transaction2.full_clean()  # This triggers validation
    
    def test_mpesa_code_normalization(self):
        """Test M-Pesa code is normalized to uppercase"""
        transaction = Transaction.objects.create(
            member=self.member,
            amount=Decimal('1000.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='abc1234567'
        )
        
        self.assertEqual(transaction.mpesa_code, 'ABC1234567')
    
    def test_verify_transaction(self):
        """Test verifying a transaction"""
        transaction = Transaction.objects.create(
            member=self.member,
            amount=Decimal('1000.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='ABC1234567'
        )
        
        transaction.verify(self.user)
        
        self.assertEqual(transaction.status, 'VERIFIED')
        self.assertEqual(transaction.verified_by, self.user)
        self.assertIsNotNone(transaction.verified_at)
    
    def test_member_required_for_contribution(self):
        """Test that member is required for non-expense transactions"""
        with self.assertRaises(ValidationError):
            transaction = Transaction(
                amount=Decimal('1000.00'),
                transaction_type='CONTRIBUTION',
                mpesa_code='ABC1234567'
            )
            transaction.full_clean()


class ChamaGroupModelTest(TestCase):
    """Tests for the ChamaGroup model"""
    
    def setUp(self):
        """Set up test data"""
        self.group = ChamaGroup.objects.create(
            name='Test Chama',
            description='A test savings group',
            monthly_contribution_amount=Decimal('1000.00')
        )
        
        self.member1 = Member.objects.create(
            name='Member One',
            phone_number='+254712345678',
            role='MEMBER'
        )
        
        self.member2 = Member.objects.create(
            name='Member Two',
            phone_number='+254722334455',
            role='MEMBER'
        )
    
    def test_group_creation(self):
        """Test creating a Chama group"""
        self.assertEqual(self.group.name, 'Test Chama')
        self.assertEqual(self.group.monthly_contribution_amount, Decimal('1000.00'))
    
    def test_calculate_total_balance_empty(self):
        """Test Business Logic Rule 3: Group Balance - no transactions"""
        balance = self.group.calculate_total_balance()
        self.assertEqual(balance, Decimal('0.00'))
    
    def test_calculate_total_balance_with_transactions(self):
        """Test Business Logic Rule 3: Group Balance - with transactions"""
        # Member 1 contribution
        Transaction.objects.create(
            member=self.member1,
            amount=Decimal('1000.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='ABC1234567',
            status='VERIFIED'
        )
        
        # Member 2 contribution
        Transaction.objects.create(
            member=self.member2,
            amount=Decimal('1000.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='DEF1234567',
            status='VERIFIED'
        )
        
        # Group expense
        Transaction.objects.create(
            amount=Decimal('500.00'),
            transaction_type='EXPENSE',
            mpesa_code='GHI1234567',
            status='VERIFIED'
        )
        
        # Payout to member 1
        Transaction.objects.create(
            member=self.member1,
            amount=Decimal('300.00'),
            transaction_type='PAYOUT',
            mpesa_code='JKL1234567',
            status='VERIFIED'
        )
        
        balance = self.group.calculate_total_balance()
        # 1000 + 1000 - 500 - 300 = 1200
        self.assertEqual(balance, Decimal('1200.00'))
    
    def test_calculate_total_balance_with_fines(self):
        """Test Business Logic Rule 3: Group Balance - fines add to balance"""
        # Member 1 contribution
        Transaction.objects.create(
            member=self.member1,
            amount=Decimal('1000.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='ABC1234567',
            status='VERIFIED'
        )
        
        # Fine from member 2
        Transaction.objects.create(
            member=self.member2,
            amount=Decimal('100.00'),
            transaction_type='FINE',
            mpesa_code='FIN1234567',
            status='VERIFIED'
        )
        
        # Payout to member 1
        Transaction.objects.create(
            member=self.member1,
            amount=Decimal('200.00'),
            transaction_type='PAYOUT',
            mpesa_code='PAY1234567',
            status='VERIFIED'
        )
        
        balance = self.group.calculate_total_balance()
        # 1000 (contribution) + 100 (fine) - 200 (payout) = 900
        self.assertEqual(balance, Decimal('900.00'))
    
    def test_get_total_fines(self):
        """Test getting total fines collected"""
        # Add fines
        Transaction.objects.create(
            member=self.member1,
            amount=Decimal('50.00'),
            transaction_type='FINE',
            mpesa_code='ABC1234567',
            status='VERIFIED'
        )
        
        Transaction.objects.create(
            member=self.member2,
            amount=Decimal('100.00'),
            transaction_type='FINE',
            mpesa_code='DEF1234567',
            status='VERIFIED'
        )
        
        fines = self.group.get_total_fines()
        self.assertEqual(fines, Decimal('150.00'))


class BusinessLogicIntegrationTest(TestCase):
    """Integration tests for all 5 business logic rules"""
    
    def setUp(self):
        """Set up comprehensive test scenario"""
        self.treasurer_user = User.objects.create_user(
            email='treasurer@chama.com',
            password='testpass123',
            first_name='John',
            last_name='Treasurer'
        )
        
        self.group = ChamaGroup.objects.create(
            name='Our Chama',
            monthly_contribution_amount=Decimal('2000.00')
        )
        
        self.treasurer = Member.objects.create(
            name='John Treasurer',
            phone_number='+254712345678',
            role='TREASURER',
            user=self.treasurer_user
        )
        
        self.member = Member.objects.create(
            name='Jane Member',
            phone_number='+254722334455',
            role='MEMBER'
        )
    
    def test_complete_workflow(self):
        """Test complete workflow: Log contribution, verify, check balances"""
        # Step 1: Treasurer logs a contribution
        contribution = Transaction.objects.create(
            member=self.member,
            amount=Decimal('2000.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='MPE1234567',
            created_by=self.treasurer_user
        )
        
        # Verify it's pending
        self.assertEqual(contribution.status, 'PENDING')
        
        # Step 2: Verify the contribution
        contribution.verify(self.treasurer_user)
        self.assertEqual(contribution.status, 'VERIFIED')
        
        # Step 3: Check member balance (Rule 2)
        member_balance = self.member.calculate_net_balance()
        self.assertEqual(member_balance, Decimal('2000.00'))
        
        # Step 4: Check member payment status (Rule 5)
        payment_status = self.member.get_payment_status(
            expected_amount=self.group.monthly_contribution_amount
        )
        self.assertEqual(payment_status, 'PAID')
        
        # Step 5: Check group balance (Rule 3)
        group_balance = self.group.calculate_total_balance()
        self.assertEqual(group_balance, Decimal('2000.00'))
    
    def test_duplicate_prevention(self):
        """Test Rule 1: Duplicate M-Pesa codes are prevented"""
        # Create first transaction
        Transaction.objects.create(
            member=self.member,
            amount=Decimal('2000.00'),
            transaction_type='CONTRIBUTION',
            mpesa_code='MPE1234567'
        )
        
        # Attempt to create duplicate should fail
        with self.assertRaises(ValidationError):
            duplicate = Transaction(
                member=self.member,
                amount=Decimal('2000.00'),
                transaction_type='CONTRIBUTION',
                mpesa_code='MPE1234567'
            )
            duplicate.full_clean()
    
    def test_admin_access_control(self):
        """Test Rule 4: Admin access logic"""
        # Treasurer should have admin access
        self.assertTrue(self.treasurer.is_admin_or_treasurer())
        
        # Regular member should not
        self.assertFalse(self.member.is_admin_or_treasurer())
