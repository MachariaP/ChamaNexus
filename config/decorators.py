# config/decorators.py
"""
Custom decorators for handling authentication and CSRF.
"""

from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from functools import wraps
from django.conf import settings

def csrf_exempt_for_api(view_func):
    """
    Decorator to exempt CSRF for specific API endpoints.
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Check if this URL should be CSRF exempt
        for pattern in settings.CSRF_EXEMPT_URLS:
            if request.path.startswith(pattern):
                return csrf_exempt(view_func)(request, *args, **kwargs)
        return view_func(request, *args, **kwargs)
    return wrapped_view

def ensure_csrf_for_api(view_func):
    """
    Decorator to ensure CSRF cookie is set for API endpoints.
    """
    @wraps(view_func)
    @ensure_csrf_cookie
    def wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapped_view
