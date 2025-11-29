from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserProfileViewSet, PasswordResetView, PasswordResetConfirmView, HealthCheckView

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserProfileViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    
    # Password reset endpoints
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # Health check
    path('health/', HealthCheckView.as_view(), name='health-check'),
]

# Add token authentication URLs (DRF built-in)
urlpatterns += [
    path('api-token-auth/', obtain_auth_token, name ='api_token_auth' ),
]
