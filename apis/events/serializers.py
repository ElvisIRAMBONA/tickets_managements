from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.events.models import Event, StatusChoices
from apps.halls.models import Halls
from apps.users.models import CustomUser


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the Event model."""

    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(is_organizer=True)
    )
    hall = serializers.PrimaryKeyRelatedField(queryset=Halls.objects.all())
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    seats_available = serializers.IntegerField(read_only=True)
    total_revenue = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "user",
            "title",
            "description",
            "capacity",
            "price",
            "date",
            "end_date",
            "hall",
            "seats_available",
            "image",
            "status",
            "created_at",
            "updated_at",
            "total_revenue",
        ]
        read_only_fields = ("seats_available", "total_revenue")

    def get_total_revenue(self, obj):
        """Calculate the total revenue for the event."""
        return obj.get_total_revenue()

    def validate(self, data):
        """Validate event data before creation or update."""
        if data["date"] >= data["end_date"]:
            raise serializers.ValidationError(
                {"end_date": _("end_date must be superior to start_date")}
            )

        hall = data.get("hall")
        if hall and data.get("capacity", 0) > hall.capacity:
            raise serializers.ValidationError(
                {
                    "capacity": _(
                        "available seats can't be more than the hall's capacity"
                    )
                }
            )

        if data["date"] < timezone.now():
            raise serializers.ValidationError(
                {"date": _("event date can't be in the past")}
            )

        return data

    def create(self, validated_data):
        """Create an event with seat availability management."""
        event = Event.objects.create(**validated_data)
        event.seats_available = event.capacity if event.capacity else 0
        event.save()
        return event

    def update(self, instance, validated_data):
        """Update an event's details."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update available seats and status
        tickets_sold = instance.get_total_tickets_sold()
        instance.seats_available = (
            max(0, instance.capacity - tickets_sold) if instance.capacity else 0
        )

        if instance.seats_available <= 0:
            instance.status = StatusChoices.SOLD_OUT

        if (
            instance.date < timezone.now()
            and instance.status == StatusChoices.PUBLISHED
        ):
            instance.status = StatusChoices.FINISHED

        instance.save()
        return instance
