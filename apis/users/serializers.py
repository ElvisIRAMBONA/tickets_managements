from django.contrib.auth import password_validation
from rest_framework import serializers

from apps.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle CustomUser."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        validators=[password_validation.validate_password],
    )
    full_name = serializers.SerializerMethodField(read_only=True)
    user_type = serializers.SerializerMethodField(read_only=True)
    is_complete_profile = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "is_organizer",
            "is_attendee",
            "password",
            "full_name",
            "user_type",
            "is_complete_profile",
        ]
        read_only_fields = [
            "id",
            "full_name",
            "user_type",
            "is_complete_profile",
        ]

    def get_full_name(self, obj):
        """Retourne le nom complet de l'utilisateur."""
        return obj.get_full_name()

    def get_user_type(self, obj):
        """Retourne le type de l'utilisateur."""
        return obj.get_user_type()

    def create(self, validated_data):
        """Crée un nouvel utilisateur avec mot de passe haché."""
        password = validated_data.pop("password")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Met à jour un utilisateur existant."""
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
