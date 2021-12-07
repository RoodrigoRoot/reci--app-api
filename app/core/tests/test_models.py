from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_with_email_succesfully(self):
        """Test create a new user with an email is succesful"""
        email = 'test@algo.com'
        password = "Testpass123"
        name = "testname"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test the email for a new user is normalized"""
        email = 'test@ALGO.COM'
        user = get_user_model()
        password = "Testpass123"
        name = "Other name"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name
        )
        self.assertEqual(user.email, email.lower())

    def tests_new_user_invalid_email(self):
        """Test creating usert witn no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234', name="algo")

    def tests_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email='algo@algo.com',
            password='tests123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
