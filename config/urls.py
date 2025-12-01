"""
URL configuration for ChamaNexus project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import CSRF utility views
from config.csrf_utils import csrf_token_view

# ============================================================================
# API URL Patterns
# ============================================================================

api_v1_patterns = [
    # CSRF token endpoint
    path('csrf-token/', csrf_token_view, name='csrf-token'),
    
    # Accounts app
    path('accounts/', include('accounts.urls')),
    
    # Add other apps here when created
    # path('chamas/', include('chamas.urls')),
    # path('members/', include('members.urls')),
]

# ============================================================================
# Main URL Patterns
# ============================================================================

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # API v1 endpoints
    path('api/v1/', include(api_v1_patterns)),
]

# ============================================================================
# Development-only URLs
# ============================================================================

if settings.DEBUG:
    # Serve static files in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
