from django.contrib.auth import password_validation
from rest_framework import serializers

from apps.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser Model."""

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
        """Return full name"""
        return obj.get_full_name()

    def get_user_type(self, obj):
        """Return type of user"""
        return obj.get_user_type()

    def create(self, validated_data):
        """Create a new user with a hashed password"""
        password = validated_data.pop("password")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """update the existing user"""
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
