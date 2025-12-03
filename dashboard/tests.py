"""
Tests for dashboard app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class DashboardViewSetTestCase(TestCase):
    """Test cases for DashboardViewSet"""

    def setUp(self):
        """Set up test client and create test users"""
        self.client = APIClient()
        
        # Create a regular user
        self.member_user = User.objects.create_user(
            email='member@test.com',
            username='member@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            is_verified=True
        )
        
        # Create a staff user (treasurer)
        self.staff_user = User.objects.create_user(
            email='treasurer@test.com',
            username='treasurer@test.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith',
            is_staff=True,
            is_verified=True
        )

    def test_dashboard_summary_requires_authentication(self):
        """Test that dashboard summary requires authentication"""
        response = self.client.get('/api/v1/dashboard/summary/')
        # DRF returns 403 Forbidden for unauthenticated requests
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_member_dashboard_summary(self):
        """Test that member user can access dashboard summary"""
        self.client.force_authenticate(user=self.member_user)
        response = self.client.get('/api/v1/dashboard/summary/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('personal_balance', response.data)
        self.assertIn('group_balance', response.data)
        self.assertIn('recent_transactions', response.data)

    def test_treasurer_dashboard_summary(self):
        """Test that treasurer user can access dashboard summary"""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get('/api/v1/dashboard/summary/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('group_summary', response.data)
        self.assertIn('defaulters', response.data)
        self.assertIn('pending_actions', response.data)
