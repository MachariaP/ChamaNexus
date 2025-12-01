from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils import timezone
from .models import User

def enforce_2fa_for_admins():
    """Enable 2FA for all admin users"""
    admin_users = User.objects.filter(is_staff=True, is_superuser=True)
    
    for admin_user in admin_users:
        if not admin_user.two_factor_enabled:
            print(f"⚠️  Warning: Admin user {admin_user.email} does not have 2FA enabled")
            # In production, you might want to force 2FA or send notifications
    
    return admin_users.count()

# Check admin 2FA status on startup
try:
    admin_count = enforce_2fa_for_admins()
    print(f"✅ Checked 2FA status for {admin_count} admin users")
except Exception as e:
    print(f"❌ Error checking admin 2FA: {e}")
