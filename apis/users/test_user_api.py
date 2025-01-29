from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.users.models import CustomUser


class UserCreationTestCase(APITestCase):
    """Test case for user creation"""

    def setUp(self):
        self.create_user_url = reverse("register")
        self.valid_user_data = {
            "username": "Elvis257",
            "password": "Nibizi2576",
            "email": "presira857@gmail.com",
            "first_name": "IRAMBONA",
            "last_name": "Elvis",
            "phone_number": "+1234567890",
            "address": "123 Main Street",
            "is_organizer": False,
            "is_attendee": True,
        }
        self.invalid_user_data = {
            "username": "",
            "password": "123",  # Password trop court
            "email": "invalid-email",  # Email invalide
        }

    def test_create_user_with_valid_data(self):
        """Test creating a user with valid data"""
        response = self.client.post(self.create_user_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("username", response.data)
        self.assertEqual(response.data["username"], self.valid_user_data["username"])
     #   self.assertTrue(CustomUser.objects.filter(username="NewUser").exists())

    # def test_create_user_with_invalid_data(self):
    #     """Test creating a user with invalid data"""
    #     response = self.client.post(self.create_user_url, self.invalid_user_data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("username", response.data)
    #     self.assertIn("email", response.data)

    # def test_create_user_without_required_fields(self):
    #     """Test creating a user without required fields"""
    #     response = self.client.post(self.create_user_url, {})
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("username", response.data)
    #     self.assertIn("password", response.data)
    #     self.assertIn("email", response.data)
