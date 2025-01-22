from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models"""

    def test_create_user_with_email(self):
        email = "test@example.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_with_normalized_email(self):
        """Failed while creating user with normalized email"""
        SAMPLE_EMAILS = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in SAMPLE_EMAILS:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_contractor_without_email_raises_error(self):
        """Failed to test  new contractor without email raises."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "blankemail")

    def test_create_super_user(self):
        user = get_user_model().objects.create_superuser(
            email="superuser@example.com",
            password="superuser123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
