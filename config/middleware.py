"""
Custom middleware for handling CSRF in API requests.
"""

from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings
import re
import logging

logger = logging.getLogger(__name__)


class CsrfExemptApiMiddleware(CsrfViewMiddleware):
    """
    Custom CSRF middleware that exempts certain API endpoints from CSRF protection.
    
    This middleware extends Django's CsrfViewMiddleware and checks configured patterns
    before applying CSRF validation. It should REPLACE django.middleware.csrf.CsrfViewMiddleware
    in MIDDLEWARE settings.
    """
    
    def __init__(self, get_response):
        """
        Initialize middleware and compile CSRF exempt patterns for performance.
        """
        super().__init__(get_response)
        # Get patterns from settings
        pattern_strings = getattr(settings, 'API_CSRF_EXEMPT_PATTERNS', None)
        
        # Warn if patterns are not configured
        if pattern_strings is None:
            logger.warning(
                'API_CSRF_EXEMPT_PATTERNS is not configured in settings. '
                'CSRF protection will be applied to all endpoints.'
            )
            self.compiled_patterns = []
        else:
            # Compile patterns once during initialization for better performance
            self.compiled_patterns = []
            for pattern in pattern_strings:
                try:
                    self.compiled_patterns.append(re.compile(pattern))
                except re.error as e:
                    logger.error(
                        f'Invalid regex pattern in API_CSRF_EXEMPT_PATTERNS: "{pattern}". '
                        f'Error: {e}. This pattern will be skipped.'
                    )
    
    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        Process view and check if it should be CSRF exempt based on URL patterns.
        """
        # Check if this path matches any of the CSRF exempt patterns
        for pattern in self.compiled_patterns:
            # Use fullmatch to ensure complete path matching and prevent bypass
            if pattern.fullmatch(request.path):
                # Skip CSRF validation for this request
                return None
        
        # Otherwise, use the default CSRF protection
        return super().process_view(request, callback, callback_args, callback_kwargs)
