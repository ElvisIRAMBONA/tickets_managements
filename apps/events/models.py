from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.halls.models import Halls
from apps.users.models import CustomUser


class StatusChoices(models.TextChoices):
    DRAFT = "DRAFT", _("Draft")
    PUBLISHED = "PUBLISHED", _("Published")
    CANCELLED = "CANCELLED", _("Canceled")
    SOLD_OUT = "SOLD_OUT", _("Sold out")
    FINISHED = "FINISHED", _("Finished")


class Event(models.Model):
    user = models.ForeignKey(
        CustomUser,
        limit_choices_to={"is_organizer": True},
        null=True,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name=_("organizer"),
    )
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    capacity = models.PositiveIntegerField(
        _("capacity"), null=True, help_text=_("Number of available seats")
    )
    price = models.DecimalField(
        _("price"), max_digits=8, decimal_places=2, help_text=_("Ticket price")
    )
    date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))
    hall = models.ForeignKey(
        Halls,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name=_("hall"),
    )
    seats_available = models.PositiveIntegerField(
        _("available seats"), null=True, blank=True
    )
    image = models.ImageField(
        upload_to="event_images/",
        null=True,
        blank=True,
        default="event_images/default.jpg",
    )

    status = models.CharField(
        _("status"),
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )
    created_at = models.DateTimeField(_("created at"), default=timezone.now)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        indexes = [
            models.Index(fields=["date", "status"]),
            models.Index(fields=["status"]),
        ]

    def clean(self):
        if self.date and self.end_date and self.end_date <= self.date:
            raise ValidationError(
                {"end_date": _("end_date must be superior to start_date")}
            )
        if (
            self.hall
            and self.hall.capacity
            and self.capacity
            and self.capacity > self.hall.capacity
        ):
            raise ValidationError(
                {
                    "capacity": _(
                        f"Available seats can't be more than the hall's capacity ({self.hall.capacity})"
                    )
                }
            )
        if self.date and self.date < timezone.now():
            raise ValidationError({"date": _("Event date can't be in the past")})

    def save(self, *args, **kwargs):
        """Save data and update."""
        if not self.capacity and self.hall:
            self.capacity = self.hall.capacity

        if not self.pk:
            self.seats_available = self.capacity if self.capacity else 0
        else:
            tickets_sold = self.get_total_tickets_sold()
            self.seats_available = (
                max(0, self.capacity - tickets_sold) if self.capacity else 0
            )

        if self.seats_available <= 0:
            self.status = StatusChoices.SOLD_OUT

        if self.date < timezone.now() and self.status == StatusChoices.PUBLISHED:
            self.status = StatusChoices.FINISHED

        super().save(*args, **kwargs)

    def get_total_tickets_sold(self):
        """Return the number of sold tickets."""
        return self.tickets.filter(status="CONFIRMED").count()

    def get_total_revenue(self):
        """Return the total amount."""
        return self.tickets.filter(status="CONFIRMED").aggregate(
            total=models.Sum("total_price")
        )["total"] or Decimal("0.00")

    def is_finished(self):
        #verify if the event has not already finished
        self.end_date < timezone.now()

    def is_available(self):
        """Verify if the event is available."""
        return (
            self.status == StatusChoices.PUBLISHED
            and self.seats_available > 0
            and not self.is_finished
        )

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%d/%m/%Y %H:%M')}"
