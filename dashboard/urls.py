"""
URL configuration for dashboard app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dashboard.views.dashboard_views import DashboardViewSet

router = DefaultRouter()
router.register(r'', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
