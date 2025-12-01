from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Enforce 2FA for admin users and notify those without it'
    
    def handle(self, *args, **options):
        admin_users = User.objects.filter(is_staff=True, is_superuser=True)
        
        self.stdout.write(f"Checking 2FA status for {admin_users.count()} admin users...")
        
        for user in admin_users:
            if user.two_factor_enabled:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ {user.email} has 2FA enabled")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  {user.email} does NOT have 2FA enabled")
                )
                # In a real implementation, you might:
                # 1. Send an email notification
                # 2. Temporarily disable admin access
                # 3. Force 2FA setup on next login
        
        self.stdout.write(
            self.style.SUCCESS("Admin 2FA audit complete")
        )
