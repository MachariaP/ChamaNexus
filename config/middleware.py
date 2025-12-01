"""
Custom middleware for handling CSRF in API requests.
"""

from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings
import re


class CsrfExemptApiMiddleware:
    """
    Middleware to exempt certain API endpoints from CSRF protection.
    
    Add this to your MIDDLEWARE setting after CsrfViewMiddleware.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if this path should be CSRF exempt
        for pattern in settings.API_CSRF_EXEMPT_PATTERNS:
            if re.match(pattern, request.path):
                # Mark request as CSRF exempt
                request.csrf_exempt = True
                break
        
        return self.get_response(request)
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Process view before it's called.
        """
        # Apply CSRF exemption based on patterns
        for pattern in settings.API_CSRF_EXEMPT_PATTERNS:
            if re.match(pattern, request.path):
                # Exempt from CSRF protection
                request.csrf_exempt = True
                break
        return None
