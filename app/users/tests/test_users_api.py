from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user API (public)"""
    def setUp(self) -> None:
        self.client = APIClient()

    def tests_create_valid_user_success(self):
        """Test creating user with valid payload is succesful"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpas123',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def tests_user_exists(self):
        """Test Creating a user that already exists fail"""
        payload = {'email': 'test@test.com', 'password': 'testpas123'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def tests_password_too_short(self):
        """Test  that the password must be be more than 5 characters"""
        payload = {'email': 'algo@test.com', 'password': 'pos', 'name':'algo'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def tests_create_token_for_user(self):
        """Test that a token is created for the user"""

        payload = {'email': 'test@test.com', 'password': 'test'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def tests_create_token_invalid_credential(self):
        """Test that token is not create if invalid credential are given"""
        create_user(email='test@londonappdev.com', password='testpass')
        payload = {'email': 'test@test1.com', 'password': 'testpas1123', 'name': 'algo'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def tests_create_token_no_user(self):
        """Test that token is not created if user doesn't exists"""
        payload = {'email': 'test@test.com', 'password': 'testpas123', 'name': 'algo'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def tests_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'al', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, 400)


