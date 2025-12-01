"""
URL configuration for ChamaNexus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as auth_views

# Import CSRF utility views
from config.csrf_utils import csrf_token_view, csrf_token_refresh_view
# Import health check from accounts
from accounts.views import HealthCheckView

# ============================================================================
# API URL Patterns
# ============================================================================

api_patterns = [
    # Authentication endpoints
    path('auth/', include('rest_framework.urls')),  # Session auth endpoints
    path('auth-token/', auth_views.obtain_auth_token),  # Token auth endpoint
    
    # CSRF endpoints
    path('csrf-token/', csrf_token_view, name='csrf_token'),
    path('csrf-token/refresh/', csrf_token_refresh_view, name='csrf_token_refresh'),
    
    # Health check endpoint
    path('health-check/', HealthCheckView.as_view(), name='health_check'),
    
    # App-specific endpoints
    path('accounts/', include('accounts.urls')),
    # path('chamas/', include('chamas.urls')),  # Uncomment when ready
    # path('members/', include('members.urls')),  # Uncomment when ready
]

# ============================================================================
# Main URL Patterns
# ============================================================================

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # API v1 endpoints
    path('api/v1/', include(api_patterns)),
    
    # API documentation (optional - for Swagger/Redoc)
    # path('api/docs/', include_docs_urls(title='ChamaNexus API')),
]

# ============================================================================
# Development-only URLs
# ============================================================================

if settings.DEBUG:
    # Serve static files in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Debug toolbar (optional)
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
    
    # API documentation (Swagger/Redoc)
    try:
        from rest_framework.documentation import include_docs_urls
        from drf_yasg.views import get_schema_view
        from drf_yasg import openapi
        from rest_framework import permissions
        
        schema_view = get_schema_view(
            openapi.Info(
                title="ChamaNexus API",
                default_version='v1',
                description="API documentation for ChamaNexus application",
                terms_of_service="https://www.chamanexus.com/terms/",
                contact=openapi.Contact(email="contact@chamanexus.com"),
                license=openapi.License(name="BSD License"),
            ),
            public=True,
            permission_classes=(permissions.AllowAny,),
        )
        
        urlpatterns += [
            path('api/docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            path('api/docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
            path('api/docs/', include_docs_urls(title='ChamaNexus API')),
        ]
    except ImportError:
        # Swagger/Redoc not installed
        pass

# ============================================================================
# Error Handlers
# ============================================================================

# Custom error handlers (optional)
handler400 = 'config.views.bad_request'
handler403 = 'config.views.permission_denied'
handler404 = 'config.views.page_not_found'
handler500 = 'config.views.server_error'
