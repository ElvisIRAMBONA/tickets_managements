from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

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

        # Verify if event is available
        if data["status"] == Ticket.StatusChoices.CONFIRMED:
            event = data["event"]
            if not event.is_available():
                raise serializers.ValidationError(
                    _("The event is not available for booking")
                )

        # Verify if event has available seats
        if data["status"] == Ticket.StatusChoices.CONFIRMED:
            if event.seats_available <= 0:
                raise serializers.ValidationError(
                    _("Plus de places disponibles pour cet événement.")
                )

        return data

    def create(self, validated_data):
        """Create a ticket"""
        # be sure for the generation of ticket for creation
        validated_data[
            "ticket_number"
        ] = Ticket.objects.create().generate_ticket_number()
        ticket = Ticket.objects.create(**validated_data)
        return ticket

    def update(self, instance, validated_data):
        """update tickets infos"""
        # update infos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # if the status is confirmed, update place and available places
        if instance.status == Ticket.StatusChoices.CONFIRMED:
            instance.total_price = instance.event.price
            instance.event.seats_available -= 1
            instance.event.save()

        instance.save()
        return instance
