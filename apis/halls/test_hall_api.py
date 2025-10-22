from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone

from apps.halls.models import Halls
from apps.users.models import CustomUser
from apps.events.models import Event


class HallCreateViewTest(TestCase):
    """Test the HallCreateView for creating a hall"""

    def setUp(self):
        self.client = APIClient()

        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

        self.client.force_authenticate(user=self.user)

        self.hall = Halls.objects.create(
        name="Test Hall",
        capacity=100,
        location="123 Test Ave",
        is_active=True
        )

        self.event = Event.objects.create(
            title="Test Event",
            description="Test event description",
            price=50.0,
            capacity=100,
            date=timezone.now() + timezone.timedelta(days=1),
            status="PUBLISHED",
            end_date=timezone.now() + timezone.timedelta(days=2),
            hall=self.hall 
        )

        # Remplace 'halls:create' par le bon nom de route défini dans ton urls.py
        self.create_hall_url = reverse("halls:create")

        self.valid_payload = {
            "name": "Conference Hall",
            "capacity": 150,
            "location": "456 Elm Street",
            "is_active": True,
        }

    def tearDown(self):
        """Nettoyer les données après chaque test"""
        Halls.objects.all().delete()
        Event.objects.all().delete()
        CustomUser.objects.all().delete()

    def test_create_hall_success(self):
        """Test creating a hall with valid data"""
        response = self.client.post(self.create_hall_url, self.valid_payload, format="json")
        print("Response status:", response.status_code)
        print("Response data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        hall = Halls.objects.first()
        self.assertIsNotNone(hall, "Aucun objet Halls n’a été créé.")
        self.assertEqual(hall.name, self.valid_payload["name"])
        self.assertEqual(hall.capacity, self.valid_payload["capacity"])
        self.assertEqual(hall.location, self.valid_payload["location"])
        self.assertTrue(hall.is_active)
