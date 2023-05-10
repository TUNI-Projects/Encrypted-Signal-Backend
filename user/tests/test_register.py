from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class RegisterAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_user_success(self):
        url = reverse('register')
        data = {
            'email': 'testuser@example.com',
            'password': 'Test@1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 201)
        self.assertEqual(response.data['email'], data['email'])
