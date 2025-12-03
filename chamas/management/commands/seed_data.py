"""
Management command to seed sample data for testing and development.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import timedelta
import random

from chamas.models import Member, Transaction, ChamaGroup

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample Chama data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Transaction.objects.all().delete()
            Member.objects.all().delete()
            ChamaGroup.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared'))

        # Create or get Chama Group
        group, created = ChamaGroup.objects.get_or_create(
            name='Jamii Savings Group',
            defaults={
                'description': 'A community savings group focused on empowering members through collective savings and loans',
                'monthly_contribution_amount': Decimal('5000.00')
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created Chama Group: {group.name}'))
        else:
            self.stdout.write(f'Using existing Chama Group: {group.name}')

        # Create test users if they don't exist
        users_data = [
            {'email': 'treasurer@chamanexus.com', 'first_name': 'Sarah', 'last_name': 'Mwangi', 'is_staff': True},
            {'email': 'john@chamanexus.com', 'first_name': 'John', 'last_name': 'Kamau', 'is_staff': False},
            {'email': 'mary@chamanexus.com', 'first_name': 'Mary', 'last_name': 'Wanjiku', 'is_staff': False},
            {'email': 'peter@chamanexus.com', 'first_name': 'Peter', 'last_name': 'Otieno', 'is_staff': False},
            {'email': 'jane@chamanexus.com', 'first_name': 'Jane', 'last_name': 'Muthoni', 'is_staff': False},
            {'email': 'david@chamanexus.com', 'first_name': 'David', 'last_name': 'Kiprop', 'is_staff': False},
            {'email': 'grace@chamanexus.com', 'first_name': 'Grace', 'last_name': 'Akinyi', 'is_staff': False},
        ]

        users = {}
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_staff': user_data['is_staff'],
                    'is_active': True,
                    'is_verified': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.email}'))
            users[user_data['email']] = user

        # Create members linked to users
        members_data = [
            {
                'user': users['treasurer@chamanexus.com'],
                'name': 'Sarah Mwangi',
                'phone': '+254712345670',
                'role': 'TREASURER'
            },
            {
                'user': users['john@chamanexus.com'],
                'name': 'John Kamau',
                'phone': '+254712345671',
                'role': 'MEMBER'
            },
            {
                'user': users['mary@chamanexus.com'],
                'name': 'Mary Wanjiku',
                'phone': '+254712345672',
                'role': 'MEMBER'
            },
            {
                'user': users['peter@chamanexus.com'],
                'name': 'Peter Otieno',
                'phone': '+254712345673',
                'role': 'MEMBER'
            },
            {
                'user': users['jane@chamanexus.com'],
                'name': 'Jane Muthoni',
                'phone': '+254712345674',
                'role': 'MEMBER'
            },
            {
                'user': users['david@chamanexus.com'],
                'name': 'David Kiprop',
                'phone': '+254712345675',
                'role': 'MEMBER'
            },
            {
                'user': users['grace@chamanexus.com'],
                'name': 'Grace Akinyi',
                'phone': '+254712345676',
                'role': 'MEMBER'
            },
        ]

        members = []
        for member_data in members_data:
            member, created = Member.objects.get_or_create(
                user=member_data['user'],
                defaults={
                    'name': member_data['name'],
                    'phone_number': member_data['phone'],
                    'role': member_data['role'],
                    'status': 'ACTIVE'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created member: {member.name}'))
            members.append(member)

        # Create sample transactions
        now = timezone.now()
        transaction_counter = 1

        # Generate transactions for the last 3 months
        for month_offset in range(3):
            month_date = now - timedelta(days=30 * month_offset)
            
            # Each member makes a contribution
            for member in members:
                if Member.objects.filter(pk=member.pk).exists():  # Verify member still exists
                    # Monthly contribution
                    mpesa_code = f'ABC{transaction_counter:07d}'
                    try:
                        Transaction.objects.create(
                            member=member,
                            amount=Decimal('5000.00'),
                            date=month_date - timedelta(days=random.randint(0, 5)),
                            transaction_type='CONTRIBUTION',
                            mpesa_code=mpesa_code,
                            status='VERIFIED',
                            description=f'Monthly contribution for {month_date.strftime("%B %Y")}',
                            created_by=users['treasurer@chamanexus.com'],
                            verified_by=users['treasurer@chamanexus.com'],
                            verified_at=month_date
                        )
                        transaction_counter += 1
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Skipping duplicate transaction: {mpesa_code}'))

        # Add some fines for specific members (defaulters)
        fine_members = members[1:4]  # John, Mary, Peter
        for i, member in enumerate(fine_members):
            mpesa_code = f'FINE{i+1:06d}'
            try:
                Transaction.objects.create(
                    member=member,
                    amount=Decimal(str(random.randint(1000, 5000))),
                    date=now - timedelta(days=random.randint(10, 60)),
                    transaction_type='FINE',
                    mpesa_code=mpesa_code,
                    status='VERIFIED',
                    description='Late payment fine',
                    created_by=users['treasurer@chamanexus.com'],
                    verified_by=users['treasurer@chamanexus.com'],
                    verified_at=now - timedelta(days=random.randint(10, 60))
                )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Skipping duplicate fine: {mpesa_code}'))

        # Add some recent transactions (last 7 days)
        recent_members = random.sample(members, 3)
        for i, member in enumerate(recent_members):
            mpesa_code = f'REC{i+1:07d}'
            try:
                Transaction.objects.create(
                    member=member,
                    amount=Decimal('5000.00'),
                    date=now - timedelta(days=random.randint(0, 7)),
                    transaction_type='CONTRIBUTION',
                    mpesa_code=mpesa_code,
                    status='VERIFIED',
                    description='Recent contribution',
                    created_by=users['treasurer@chamanexus.com'],
                    verified_by=users['treasurer@chamanexus.com'],
                    verified_at=now - timedelta(days=random.randint(0, 7))
                )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Skipping duplicate recent transaction: {mpesa_code}'))

        # Add some payouts for members with loans
        loan_members = members[1:3]  # John and Mary
        for i, member in enumerate(loan_members):
            # Loan disbursement
            mpesa_code = f'LOAN{i+1:06d}'
            try:
                Transaction.objects.create(
                    member=member,
                    amount=Decimal('50000.00'),
                    date=now - timedelta(days=60),
                    transaction_type='PAYOUT',
                    mpesa_code=mpesa_code,
                    status='VERIFIED',
                    description='Business loan disbursement',
                    created_by=users['treasurer@chamanexus.com'],
                    verified_by=users['treasurer@chamanexus.com'],
                    verified_at=now - timedelta(days=60)
                )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Skipping duplicate loan: {mpesa_code}'))

        # Add some pending transactions
        pending_member = members[-1]
        mpesa_code = 'PEND000001'
        try:
            Transaction.objects.create(
                member=pending_member,
                amount=Decimal('5000.00'),
                date=now,
                transaction_type='CONTRIBUTION',
                mpesa_code=mpesa_code,
                status='PENDING',
                description='Pending verification',
                created_by=users['treasurer@chamanexus.com']
            )
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Skipping duplicate pending transaction: {mpesa_code}'))

        total_members = Member.objects.count()
        total_transactions = Transaction.objects.count()
        total_balance = group.calculate_total_balance()

        self.stdout.write(self.style.SUCCESS('\n=== Seeding Complete ==='))
        self.stdout.write(f'Total Members: {total_members}')
        self.stdout.write(f'Total Transactions: {total_transactions}')
        self.stdout.write(f'Total Group Balance: KES {total_balance:,.2f}')
        self.stdout.write(self.style.SUCCESS('\nYou can now test the dashboard with real data!'))
        self.stdout.write(f'\nTest users (password: password123):')
        for user_data in users_data:
            self.stdout.write(f'  - {user_data["email"]} ({"Treasurer" if user_data["is_staff"] else "Member"})')
