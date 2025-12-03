from rest_framework import permissions


class IsTreasurerOrAdmin(permissions.BasePermission):
    """
    Business Logic Rule 4: Admin Access Logic
    
    Permission class that restricts access to Treasurer or Admin roles.
    This ensures that only authorized users can log/edit transactions.
    """
    
    message = 'Only Treasurer or Admin can perform this action.'
    
    def has_permission(self, request, view):
        """
        Check if user has a member record with Treasurer or Admin role.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superusers always have permission
        if request.user.is_superuser:
            return True
        
        # Check if user has a member record with appropriate role
        from .models import Member
        
        member = Member.objects.filter(
            user=request.user,
            status='ACTIVE'
        ).first()
        
        if member and member.is_admin_or_treasurer():
            return True
        
        return False
