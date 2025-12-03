"""
URL configuration for ChamaNexus project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# ============================================================================
# Root-Level Views for Frontend Compatibility
# ============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_token_view(request):
    """Get CSRF token for API requests"""
    return JsonResponse({'csrfToken': get_token(request)})

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for monitoring"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'ChamaNexus API',
        'version': '1.0.0',
        'timestamp': 'ISO timestamp here',
        'endpoints': {
            'api_v1': '/api/v1/',
            'admin': '/admin/',
            'csrf_token': '/csrf-token/',
            'health': '/health/',
            'accounts': {
                'register': '/accounts/auth/register/',
                'login': '/accounts/auth/login/',
                'logout': '/accounts/auth/logout/',
            }
        }
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API root endpoint"""
    return JsonResponse({
        'name': 'ChamaNexus API',
        'version': '1.0.0',
        'documentation': 'Coming soon',
        'endpoints': {
            'accounts': '/accounts/',
            'csrf': '/csrf-token/',
            'health': '/health/',
            'admin': '/admin/'
        }
    })

# ============================================================================
# API URL Patterns
# ============================================================================

api_v1_patterns = [
    # CSRF token endpoint
    path('csrf-token/', csrf_token_view, name='csrf-token'),
    
    # Accounts app
    path('accounts/', include('accounts.urls')),
    
    # Chamas app
    path('chamas/', include('chamas.urls')),
    
    # Dashboard app
    #path('dashboard/', include('dashboard.urls')),
    
    # Add other apps here when created
    # path('members/', include('members.urls')),
]

# ============================================================================
# Main URL Patterns (Updated for Frontend Compatibility)
# ============================================================================

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # API v1 endpoints (versioned)
    path('api/v1/', include(api_v1_patterns)),
    
    # Root level endpoints for frontend compatibility
    path('csrf-token/', csrf_token_view, name='csrf-token-root'),
    path('health/', health_check, name='health-check'),
    path('', api_root, name='api-root'),
    
    # Include accounts at root level for frontend compatibility
    path('accounts/', include('accounts.urls')),
]

# ============================================================================
# Development-only URLs
# ============================================================================

if settings.DEBUG:
    # Serve static files in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
