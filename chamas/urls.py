from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, TransactionViewSet, ChamaGroupViewSet

# Create router for automatic URL routing
router = DefaultRouter()
router.register(r'members', MemberViewSet, basename='member')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'groups', ChamaGroupViewSet, basename='group')

app_name = 'chamas'

urlpatterns = [
    path('', include(router.urls)),
]
