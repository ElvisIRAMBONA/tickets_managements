from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.events.models import Event, StatusChoices
from apps.users.models import CustomUser
from apps.halls.models import Halls


class EventCreationTestCase(APITestCase):
    """Test case for event creation."""

    def setUp(self):
        self.create_event_url = reverse("event_create")  # Assure-toi que ce nom de route est correct.
        
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

        # Event payload
        self.valid_event_data = {
            "user": self.organizer.id,
            "title": "Sample Event",
            "description": "This is a test event.",
            "capacity": 50,
            "price": "20.00",
            "date": "2025-12-01T10:00:00Z",
            "end_date": "2025-12-01T12:00:00Z",
            "hall": self.hall.id,
            "status": StatusChoices.DRAFT
        }

    def test_create_event_success(self):
        """Test creating an event with valid data"""
        
        response = self.client.post(self.create_event_url, self.valid_event_data, format="json")
        print(response.data)  # Optionnel : utile pour debug
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.title, self.valid_event_data["title"])
        self.assertEqual(event.capacity, self.valid_event_data["capacity"])
        self.assertEqual(event.hall.id, self.valid_event_data["hall"])
        self.assertEqual(event.status, self.valid_event_data["status"])
