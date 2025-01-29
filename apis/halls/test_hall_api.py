from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.halls.models import Halls
from django.urls import reverse


class HallCreateViewTest(TestCase):
    """Test the HallCreateView for creating a hall"""

    def setUp(self):
        """Set up test client and sample data"""
        self.create_event_url = reverse("create")
        self.client = APIClient()
        self.valid_payload = {
            "name": "Conference Hall",
            "capacity": 150,
            "location": "456 Elm Street",
            "is_active": True,
        }

    def test_create_hall_success(self):
        """Test creating a hall with valid data"""
        response = self.client.post(self.create_event_url, self.valid_payload, format="json")
        print(response.data)  # Afficher la réponse pour examiner l'erreur

        hall = Halls.objects.first()
        self.assertEqual(hall.name, self.valid_payload["name"])
        self.assertEqual(hall.capacity, self.valid_payload["capacity"])
        self.assertEqual(hall.location, self.valid_payload["location"])
        self.assertTrue(hall.is_active)
