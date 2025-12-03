"""
Custom middleware for handling CSRF in API requests.
"""

from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings
import re


class CsrfExemptApiMiddleware(CsrfViewMiddleware):
    """
    Custom CSRF middleware that exempts certain API endpoints from CSRF protection.
    
    This middleware extends Django's CsrfViewMiddleware and checks configured patterns
    before applying CSRF validation. It should REPLACE django.middleware.csrf.CsrfViewMiddleware
    in MIDDLEWARE settings.
    """
    
    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        Process view and check if it should be CSRF exempt based on URL patterns.
        """
        # Check if this path matches any of the CSRF exempt patterns
        for pattern in settings.API_CSRF_EXEMPT_PATTERNS:
            if re.match(pattern, request.path):
                # Skip CSRF validation for this request
                return None
        
        # Otherwise, use the default CSRF protection
        return super().process_view(request, callback, callback_args, callback_kwargs)
