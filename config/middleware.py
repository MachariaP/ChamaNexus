# config/middleware.py
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
        api_patterns = [
            r'^/api/v1/accounts/auth/login/$',
            r'^/api/v1/accounts/auth/register/$',
            r'^/api/v1/accounts/auth/logout/$',
            r'^/api/v1/accounts/password-reset/',
            r'^/accounts/auth/login/$',
            r'^/accounts/auth/register/$',
            r'^/accounts/auth/logout/$',
            r'^/accounts/password-reset/',
        ]
        
        # Check if the current path matches any API pattern
        for pattern in api_patterns:
            if re.match(pattern, request.path):
                # Mark request as CSRF exempt
                request.csrf_exempt = True
                break
        
        return self.get_response(request)
