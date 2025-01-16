# apps/users/models.py

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Model for personnalised user.
    """

    # Validators
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="The phone number must have the format: '+999999999'. Max 12 digits.",
    )

    # Custom fields
    is_organizer = models.BooleanField(
        _("status organizer"),
        default=False,
        help_text=_("show if user can organize an event"),
    )

    is_attendee = models.BooleanField(
        _("participant status"),
        default=True,
        help_text=_("show if a user can be a participant"),
    )

    phone_number = models.CharField(
        _("phone number"),
        max_length=15,
        validators=[phone_regex],
        blank=True,
        null=True,
        help_text=_("phone number in international format"),
    )

    address = models.TextField(
        _("adress"), blank=True, null=True, help_text=_("User Address")
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"

    def get_full_name(self):
        """Return fullname"""
        full_name = super().get_full_name()
        return full_name if full_name else self.username

    def get_user_type(self):
        """Return user type."""
        if self.is_superuser:
            return "Administrator"
        elif self.is_organizer:
            return "Organizer"
        return "Participant"

    def get_tickets(self):
        """Return all users tickets."""
        return self.tickets.all()

    def get_organized_events(self):
        """Return all event organized by user."""
        if self.is_organizer:
            return self.events.all()
        return None

    @property
    def is_complete_profile(self):
        """Verify if profile is complete"""
        return bool(
            self.first_name
            and self.last_name
            and self.email
            and self.phone_number
            and self.address
        )
