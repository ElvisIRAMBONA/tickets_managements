from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.events.models import Event
from apps.tickets.models import Ticket
from apps.users.models import CustomUser


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for model ticket"""

    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    status = serializers.ChoiceField(choices=Ticket.StatusChoices.choices)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    ticket_number = serializers.CharField(max_length=50, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "event",
            "user",
            "purchase_date",
            "status",
            "total_price",
            "ticket_number",
        ]
        read_only_fields = ("total_price", "ticket_number", "purchase_date")

    def validate(self, data):
        """
        Validate data before creating/updating the ticket.
        """
        user = self.context["request"].user  # Get the authenticated user

        # Verify if the user is authenticated
        if not user.is_authenticated:
            raise PermissionDenied(_("you must login before you buy a ticket."))

        # Ensure the ticket belongs to the logged-in user
        if "user" in data and data["user"] != user:
            raise serializers.ValidationError(
                _("Vous ne pouvez pas acheter un ticket pour un autre utilisateur.")
            )

        # Get the event from data or instance
        event = data.get("event") or self.instance.event

        # Check for duplicate ticket
        if self.instance is None:  # Only for creation
            existing_ticket = Ticket.objects.filter(event=event, user=user).exists()
            if existing_ticket:
                raise serializers.ValidationError(
                    _("You already have a ticket for this event.")
                )

        # Verify if the event is available for booking
        if data["status"] == Ticket.StatusChoices.CONFIRMED:
            if not event.is_available():
                raise serializers.ValidationError(
                    _("The event is no longer available ")
                )

            # Verify if the event has available seats
            if event.seats_available <= 0:
                raise serializers.ValidationError(
                    _("No available seat for this event")
                )

        # For PENDING status, also check seats if trying to create
        if self.instance is None and data["status"] == Ticket.StatusChoices.PENDING:
            if event.seats_available <= 0:
                raise serializers.ValidationError(
                    _("No available seat for this event")
                )

        return data

    def create(self, validated_data):
        """
        Create a ticket for the authenticated user.
        """
        # Get the authenticated user
        user = self.context["request"].user
        validated_data["user"] = user

        # Generate a ticket number
        ticket = Ticket(**validated_data)
        ticket.ticket_number = ticket.generate_ticket_number()

        # Create the ticket
        ticket.save()
        return ticket

    def update(self, instance, validated_data):
        """
        Update ticket information.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If the status is confirmed, update total price and reduce available seats
        if validated_data.get("status") == Ticket.StatusChoices.CONFIRMED and instance.status != Ticket.StatusChoices.CONFIRMED:
            instance.total_price = instance.event.price
            instance.event.seats_available -= 1
            instance.event.save()

        instance.save()
        return instance
