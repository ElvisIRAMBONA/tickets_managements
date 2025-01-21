from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "username",
        "email",
        "get_full_name",
        "is_organizer",
        "is_attendee",
        "is_superuser",
        "is_active",
        "date_joined",
    )
    list_filter = (
        "is_organizer",
        "is_attendee",
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
    )
    search_fields = ("username", "email", "first_name", "last_name", "phone_number")
    ordering = ("-date_joined",)

    fieldsets = (
        ("Informations de connexion", {
            "fields": ("username", "password")
        }),
        ("Informations personnelles", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "address",
            )
        }),
        ("Statut et permissions", {
            "fields": (
                "is_organizer",
                "is_attendee",
                "is_superuser",
                "is_staff",
                "is_active",
                "groups",
                "user_permissions",
            )
        }),
        ("Dates importantes", {
            "fields": ("last_login", "date_joined")
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "address",
                "is_organizer",
                "is_attendee",
                "is_superuser",
                "is_staff",
                "is_active",
            ),
        }),
    )
