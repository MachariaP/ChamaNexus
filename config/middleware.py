# config/middleware.py
"""
Custom middleware for handling CSRF in API requests.
This allows API requests from frontend while maintaining CSRF protection for Django admin.
"""

from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings
import re

class CustomCsrfMiddleware(CsrfViewMiddleware):
    """
    Custom CSRF middleware that bypasses CSRF check for API endpoints
    that use token authentication.
    """
    
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Skip CSRF check for API endpoints using token auth
        api_pattern = re.compile(r'^/api/')
        
        # Check if it's an API request
        if api_pattern.match(request.path):
            # Check if token auth header is present
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Token '):
                return None  # Skip CSRF check for token-authenticated API requests
            
            # Check if it's a login/register endpoint (AllowAny)
            if request.path in [
                '/api/v1/accounts/auth/login/',
                '/api/v1/accounts/auth/register/',
                '/api/v1/accounts/auth/logout/',
            ]:
                return None
        
        return super().process_view(request, callback, callback_args, callback_kwargs)


class CorsMiddleware:
    """
    Custom CORS middleware for handling cross-origin requests.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Handle preflight requests
        if request.method == 'OPTIONS':
            response = self._handle_preflight(request)
        else:
            response = self.get_response(request)
        
        # Add CORS headers to all responses
        self._add_cors_headers(request, response)
        return response
    
    def _handle_preflight(self, request):
        from django.http import HttpResponse
        response = HttpResponse()
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    
    def _add_cors_headers(self, request, response):
        # Allow credentials
        response['Access-Control-Allow-Credentials'] = 'true'
        
        # Set allowed origin
        origin = request.META.get('HTTP_ORIGIN', '')
        if origin in settings.CORS_ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
