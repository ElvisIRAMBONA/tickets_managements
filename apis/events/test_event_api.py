from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.events.models import Event, StatusChoices
from apps.users.models import CustomUser
from apps.halls.models import Halls


class EventCreationTestCase(APITestCase):
    """Test case for event creation."""

    def setUp(self):
        self.create_event_url = reverse("create")
        # Create a user
        self.organizer = CustomUser.objects.create_user(
            username="organizer",
            password="StrongPass123",
            email="organizer@example.com",
            is_organizer=True,
        )

        self.client.force_authenticate(user=self.organizer)
        # Create a hall
        self.hall = Halls.objects.create(
            name="Main Hall",
            capacity=100,
            location="Test Location",
        )

        # create event
        self.valid_event_data = {
            "user": self.organizer.id,
            "title": "Sample Event",
            "description": "This is a test event.",
            "capacity": 50,
            "price": "20.00",
            "date": "2025-02-01T10:00:00Z",
            "end_date": "2025-02-01T12:00:00Z",
            "hall": self.hall.id,
            "status": "DRAFT",
        }

def test_create_hall_success(self):
    """Test creating a hall with valid data"""
    response = self.client.post(self.create_event_url, self.valid_payload, format="json")
    print(response.data)  # Afficher la réponse pour examiner l'erreur
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Halls.objects.count(), 1)
    hall = Halls.objects.first()
    self.assertEqual(hall.name, self.valid_payload["name"])
    self.assertEqual(hall.capacity, self.valid_payload["capacity"])
    self.assertEqual(hall.location, self.valid_payload["location"])
    self.assertTrue(hall.is_active)


class SearchEventsAPITestCase(APITestCase):
    def test_search_events(self):
        url = reverse('search_events')
        response = self.client.get(url, {'q': 'test', 'price_min': 10, 'price_max': 50})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)