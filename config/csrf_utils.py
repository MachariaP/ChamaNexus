"""
CSRF Utility Functions for ChamaNexus API

This module provides utility functions for handling CSRF tokens in API requests.
It helps bridge the gap between Django's CSRF protection and frontend API calls.
"""

from functools import wraps
from django.middleware.csrf import get_token, rotate_token
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from django.utils.decorators import method_decorator
from django.conf import settings
import re

# ============================================================================
# CSRF Token Management
# ============================================================================

def ensure_csrf_cookie_set(request):
    """
    Ensure that a CSRF cookie is set for the request.
    
    Args:
        request: Django HttpRequest object
    
    Returns:
        str: The CSRF token
    """
    # Get or create CSRF token
    csrf_token = get_token(request)
    
    # Rotate token if needed (optional, for security)
    if getattr(settings, 'CSRF_ROTATE_EACH_REQUEST', False):
        rotate_token(request)
    
    return csrf_token

def get_csrf_token_from_request(request):
    """
    Extract CSRF token from request headers or cookies.
    
    Args:
        request: Django HttpRequest object
    
    Returns:
        str or None: The CSRF token if found, None otherwise
    """
    # Check headers first (X-CSRFToken or X-CSRF-Token)
    csrf_token = request.headers.get('X-CSRFToken') or request.headers.get('X-CSRF-Token')
    
    # If not in headers, check cookies
    if not csrf_token:
        csrf_token = request.COOKIES.get(settings.CSRF_COOKIE_NAME)
    
    return csrf_token

def validate_csrf_token(request):
    """
    Validate CSRF token for API requests.
    
    Args:
        request: Django HttpRequest object
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # Skip CSRF validation for exempt URLs
    for pattern in getattr(settings, 'API_CSRF_EXEMPT_PATTERNS', []):
        if re.match(pattern, request.path):
            return True, None
    
    # Get CSRF token from request
    csrf_token = get_csrf_token_from_request(request)
    
    if not csrf_token:
        return False, "CSRF token missing"
    
    # Get CSRF token from session (Django's built-in validation)
    from django.middleware.csrf import _get_new_csrf_token, _sanitize_token
    
    csrf_token = _sanitize_token(csrf_token)
    
    # Check against session token
    session_csrf_token = request.META.get('CSRF_COOKIE')
    if not session_csrf_token:
        # Get or create CSRF token in session
        csrf_token = ensure_csrf_cookie_set(request)
        return True, None
    
    # Compare tokens
    if not _sanitize_token(session_csrf_token) == csrf_token:
        return False, "CSRF token invalid"
    
    return True, None

# ============================================================================
# CSRF View Functions
# ============================================================================

@require_GET
@ensure_csrf_cookie
def csrf_token_view(request):
    """
    API endpoint to get CSRF token for frontend.
    
    This endpoint sets the CSRF cookie and returns the token in JSON format.
    The frontend should call this endpoint before making POST/PUT/PATCH/DELETE requests.
    
    Returns:
        JsonResponse: Contains CSRF token
    """
    csrf_token = ensure_csrf_cookie_set(request)
    
    response_data = {
        'success': True,
        'csrfToken': csrf_token,
        'csrfCookieName': settings.CSRF_COOKIE_NAME,
        'message': 'CSRF token generated successfully'
    }
    
    # Create response
    response = JsonResponse(response_data)
    
    # Set CORS headers
    origin = request.META.get('HTTP_ORIGIN')
    if origin in getattr(settings, 'CORS_ALLOWED_ORIGINS', []):
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Credentials'] = 'true'
    
    return response

@require_POST
@csrf_exempt
def csrf_token_refresh_view(request):
    """
    API endpoint to refresh CSRF token (for security purposes).
    
    This endpoint rotates the CSRF token and returns a new one.
    Useful for sensitive operations or after authentication.
    
    Returns:
        JsonResponse: Contains new CSRF token
    """
    # Rotate CSRF token
    rotate_token(request)
    csrf_token = get_token(request)
    
    response_data = {
        'success': True,
        'csrfToken': csrf_token,
        'message': 'CSRF token refreshed successfully'
    }
    
    response = JsonResponse(response_data)
    
    # Set CORS headers
    origin = request.META.get('HTTP_ORIGIN')
    if origin in getattr(settings, 'CORS_ALLOWED_ORIGINS', []):
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Credentials'] = 'true'
    
    return response

# ============================================================================
# CSRF Middleware (Alternative approach)
# ============================================================================

class CsrfExemptMiddleware:
    """
    Custom middleware to exempt certain API endpoints from CSRF protection.
    
    This middleware should be placed after Django's CsrfViewMiddleware.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if this path should be CSRF exempt
        for pattern in getattr(settings, 'API_CSRF_EXEMPT_PATTERNS', []):
            if re.match(pattern, request.path):
                # Set CSRF cookie for exempt endpoints (optional)
                if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
                    ensure_csrf_cookie_set(request)
                break
        
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Process view before it's called.
        """
        # Check if this view should be CSRF exempt
        for pattern in getattr(settings, 'API_CSRF_EXEMPT_PATTERNS', []):
            if re.match(pattern, request.path):
                # Exempt from CSRF protection
                request.csrf_exempt = True
                break
        
        return None

# ============================================================================
# Simple decorator without wraps issue
# ============================================================================

def csrf_exempt_for_api(view_func):
    """
    Simple decorator to exempt API views from CSRF protection.
    This version doesn't cause issues with DRF routers.
    """
    view_func.csrf_exempt = True
    return view_func

def ensure_csrf_for_api(view_func):
    """
    Simple decorator to ensure CSRF cookie is set.
    """
    return ensure_csrf_cookie(view_func)
