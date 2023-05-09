from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.test import RequestFactory, TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from user.models import User
from user.motherland.login import LoginAPI


class LoginAPITestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.login_url = "/user/login/"
        # create a test user
        self.user = User.objects.create(
            email="testuser@example.com",
            password=make_password("password123")
        )

    def test_missing_required_parameter(self):
        request = self.factory.post(self.login_url, data={})
        response = LoginAPI.as_view()(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content, b'{"status": 400, "message": "Missing Required Parameter. email is required"}')

    def test_email_does_not_exist(self):
        request = self.factory.post(self.login_url, data={
            "email": "nonexistent@example.com",
            "password": "password123"
        })
        response = LoginAPI.as_view()(request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.content, b'{"status": 404, "message": "Email and password doesn\'t match!"}')

    def test_wrong_password(self):
        request = self.factory.post(self.login_url, data={
            "email": self.user.email,
            "password": "wrongpassword"
        })
        response = LoginAPI.as_view()(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content, b'{"status": 400, "message": "email and password don\'t match!"}')

    def test_successful_login(self):
        # make sure last_login is not set initially
        self.assertIsNone(self.user.last_login)

        # create a session cookie
        response = self.client.post(self.login_url, {
            "email": "testuser@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 202)
        self.assertIn(b'login successful!', response.content)

        # check that last_login was updated
        user = User.objects.get(email=self.user.email)
        self.assertIsNotNone(user.last_login)

        # check that the session cookie was set
        self.assertTrue(response.cookies.get('sessionId'))

    def test_successful_login_session_expired(self):
        # make sure last_login is not set initially
        self.assertIsNone(self.user.last_login)

        # create a session cookie with an expiration date in the past
        session_store = self.client.session
        session_store["username"] = self.user.username
        test_expiry = (timezone.now() - timedelta(days=1)).timestamp()
        session_store["_session_expiry"] = test_expiry

        session_store.save()

        # make a request to the login API to refresh the session cookie
        self.client.force_login(self.user)
        response = self.client.post(self.login_url, {
            "email": self.user.email,
            "password": "password123"
        })
        self.assertEqual(response.status_code, 202)
        self.assertIn(b'login successful!', response.content)

        # check that last_login was updated
        user = User.objects.get(email=self.user.email)
        self.assertIsNotNone(user.last_login)

        # check that the session cookie was updated
        session_store = self.client.session
        self.assertIsNotNone(session_store["_session_expiry"])
        self.assertGreater(
            session_store["_session_expiry"],  timezone.now().timestamp())
