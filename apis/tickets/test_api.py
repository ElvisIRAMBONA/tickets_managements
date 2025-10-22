from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.tickets.models import Ticket
from apps.events.models import Event
from apps.users.models import CustomUser
from apps.halls.models import Halls
from django.urls import reverse
from decimal import Decimal
import datetime
from django.utils import timezone


class TicketApiTests(APITestCase):
    """Test for tickets API"""

    @classmethod
    def setUpTestData(cls):
        """initial configuration of shared data between test ."""
        # creation of test user
        cls.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

        # Creation of hall for test
        cls.hall = Halls.objects.create(
            name="Test Hall",
            capacity=100,
            location="Test Location",
        )

        # Creation of event for test
        cls.event = Event.objects.create(
            title="Test Event",
            description="Description de l'événement",
            price=Decimal("100.00"),
            capacity=100,
            seats_available=10,
            date=timezone.make_aware(datetime.datetime.fromisoformat("2025-02-01T10:00:00")),
            end_date=timezone.make_aware(datetime.datetime.fromisoformat("2025-02-01T12:00:00")),
            hall=cls.hall,
        )

        # Generation of JWT token for user
        cls.user_token = cls.get_jwt_token(cls.user)

        # defition of useful URLs for tests
        cls.ticket_create_url = reverse("tickets:create")
        cls.ticket_management_url = reverse("tickets:ticket-list-create")

    @staticmethod
    def get_jwt_token(user):
        """Generate a JWT token for user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate_user(self):
        """Add the JWT token to the headers for authenticated requests."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")

    def test_create_ticket_success(self):
        """Test for ticket created successfully."""
        self.authenticate_user()
        data = {
            "event": self.event.id,
            "user": self.user.id,
            "status": "PENDING",
        }
        response = self.client.post(self.ticket_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "The ticket have already been created.")
        self.assertEqual(Ticket.objects.count(), 1, "one ticket must be created")
        self.assertEqual(response.data["status"], "PENDING", "event status is now PENDING.")

    def test_create_ticket_without_authentication(self):
        """Test if a user whose not authentificate can buy a ticket"""
        data = {
            "event": self.event.id,
            "user": self.user.id,
            "status": "PENDING",
        }
        response = self.client.post(self.ticket_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, "La requête aurait dû être non autorisée.")
        self.assertEqual(Ticket.objects.count(), 0, "Aucun ticket ne devrait être créé sans authentification.")

    def test_create_ticket_with_invalid_event(self):
        """Test pour la création d'un ticket avec un événement invalide."""
        self.authenticate_user()
        data = {
            "event": 999,  # ID d'un événement inexistant
            "user": self.user.id,
            "status": "PENDING",
        }
        response = self.client.post(self.ticket_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "L'événement invalide devrait être rejeté.")
        self.assertIn("event", response.data, "Le champ 'event' devrait contenir une erreur.")

    def test_create_ticket_with_no_seats_available(self):
        """Test pour la création d'un ticket lorsque les places sont épuisées."""
        self.authenticate_user()
        self.event.seats_available = 0
        self.event.save()
        data = {
            "event": self.event.id,
            "user": self.user.id,
            "status": "PENDING",
        }
        response = self.client.post(self.ticket_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Les places épuisées devraient être rejetées.")
        self.assertIn("non_field_errors", response.data, "Le champ 'non_field_errors' devrait signaler une erreur.")

    def test_create_duplicate_ticket(self):
        """Test pour empêcher la création de tickets en double."""
        self.authenticate_user()
        Ticket.objects.create(event=self.event, user=self.user, status="PENDING")
        data = {
            "event": self.event.id,
            "user": self.user.id,
            "status": "PENDING",
        }
        response = self.client.post(self.ticket_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Les doublons devraient être rejetés.")
        self.assertIn("non_field_errors", response.data, "Le champ 'non_field_errors' devrait signaler une erreur.")

    def test_get_all_tickets(self):
        """Test pour la récupération de tous les tickets."""
        self.authenticate_user()
        Ticket.objects.create(event=self.event, user=self.user, status="PENDING")
        response = self.client.get(self.ticket_management_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "La récupération des tickets aurait dû réussir.")
        self.assertEqual(len(response.data), 1, "Un seul ticket aurait dû être retourné.")

    def test_update_ticket_status(self):
        """Test pour la mise à jour du statut d'un ticket."""
        self.authenticate_user()
        ticket = Ticket.objects.create(event=self.event, user=self.user, status="PENDING")
        url = reverse("tickets:ticket-management", args=[ticket.id])
        data = {"status": "CONFIRMED"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "La mise à jour aurait dû réussir.")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "CONFIRMED", "Le statut aurait dû être mis à jour.")

    def test_delete_ticket_not_found(self):
        """Test pour la suppression d'un ticket inexistant."""
        self.authenticate_user()
        url = reverse("tickets:ticket-management", args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, "Le ticket inexistant aurait dû retourner 404.")
