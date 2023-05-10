from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User


class LoginAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='testuser@example.com',
            password='Test@1234',
            username='testuser'
        )

    def test_login_user_success(self):
        url = reverse('login')
        data = {
            'email': self.user.email,
            'password': 'Test@1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        # Check that the response includes the correct username
        self.assertEqual(response['username'], self.user.username)
        # Check that the session cookie is set
        self.assertTrue('sessionId' in response.cookies)