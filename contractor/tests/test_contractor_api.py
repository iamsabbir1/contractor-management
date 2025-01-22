from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_CONTRACTOR_URL = reverse("contractor:create")
TOKEN_URL = reverse("contractor:token")
ME_URL = reverse("contractor:me")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_contractor_succes(self):
        payload = {
            "name": "Test Contractor",
            "email": "test@example.com",
            "password": "testpass1243",
        }

        res = self.client.post(CREATE_CONTRACTOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_contractor_with_email_exists_error(self):
        """Test error returned if contractor with email exists."""
        payload = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "testpass123",
        }

        create_user(**payload)
        res = self.client.post(CREATE_CONTRACTOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "pw",
        }

        res = self.client.post(CREATE_CONTRACTOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        contractor_exists = (
            get_user_model()
            .objects.filter(
                email=payload["email"],
            )
            .exists()
        )
        self.assertFalse(contractor_exists)

    def test_create_token_for_contractor(self):
        """Test generates token for valid credentials."""
        contractor_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "test-user-password123",
        }

        create_user(**contractor_details)
        payload = {
            "email": contractor_details["email"],
            "password": contractor_details["password"],
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn(
            "token",
            res.data,
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test return errors if credentials invalid"""
        create_user(
            email="test@example.com",
            password="goodpassword",
        )

        payload = {
            "email": "test@example.com",
            "password": "badpassword",
        }
        res = self.client.post(
            TOKEN_URL,
            payload,
        )

        self.assertNotIn(
            "token",
            res.data,
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""
        payload = {
            "email": "test@example.com",
            "password": "",
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_contractor_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateContractorApiTests(TestCase):
    """Tests API request that require authentication."""

    def setUp(self):
        self.user = create_user(
            email="test@example.com",
            password="testpass123",
            name="Test Name",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in contractor"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "name": self.user.name,
                "email": self.user.email,
            },
        )

    def test_post_me_not_allowed(self):
        """Test me is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # test_user_api.py

    def test_update_contractor_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {
            "name": "Updated Name",
            "password": "newpassword123",
        }

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
