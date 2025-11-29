from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User

class EmailBackend(ModelBackend):
    """
    Authenticate using email or username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to fetch user by email or username
            user = User.objects.get(
                Q(email=username) | Q(username=username)
            )
            
            # Check if account is locked
            if user.is_account_locked():
                return None
                
            # Verify password
            if user.check_password(password):
                return user
            else:
                # Record failed attempt
                user.record_failed_login()
                
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
