# apps/halls/models.py
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Halls(models.Model):
    """Model of event hall"""

    name = models.CharField(_("name"), max_length=255, unique=True)
    image = models.ImageField(
        upload_to="event_hall_images/",
        null=True,
        blank=True,
        default="event_hall_images/default.jpg",
    )

    capacity = models.PositiveIntegerField(
        _("capacity"), help_text=_("max hall seats"), null=False
    )
    location = models.CharField(_("location"), max_length=255, help_text=_("Adress"))
    is_active = models.BooleanField(
        _("active"), default=True, help_text=_("show if hall is available")
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("hall")
        verbose_name_plural = _("halls")

    def __str__(self):
        return f"{self.name} ({self.capacity} places)"

    def get_upcoming_events(self):
        """return the upcoming events"""
        return self.events.filter(
            date__gte=timezone.now(), status="PUBLISHED"
        ).order_by("date")
