from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.halls.models import Halls


class HallSerializer(serializers.ModelSerializer):
    """Serializer for model halls."""

    image = serializers.ImageField(required=False)
    location = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Halls
        fields = ["id", "name", "image", "capacity", "location", "is_active"]
        read_only_fields = ["id"]

    def validate(self, data):
        """Validation  personnalised for hall"""
        if data["capacity"] <= 0:
            raise serializers.ValidationError(
                _("the event capacity must be a positif number")
            )
        return data
