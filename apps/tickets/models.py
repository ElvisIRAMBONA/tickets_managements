import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.events.models import Event
from apps.users.models import CustomUser


class Ticket(models.Model):
    """Modèle représentant un billet."""

    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", _("En attente")
        CONFIRMED = "CONFIRMED", _("Confirmé")
        CANCELLED = "CANCELLED", _("Annulé")

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("événement"),
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("utilisateur"),
    )
    purchase_date = models.DateTimeField(_("date d'achat"), auto_now_add=True)
    status = models.CharField(
        _("status"),
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    total_price = models.DecimalField(
        _("prix total"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        editable=False,
    )
    ticket_number = models.CharField(
        _("numéro de billet"),
        max_length=50,
        unique=True,
        editable=False,
        null=True,
    )

    class Meta:
        ordering = ["-purchase_date"]
        verbose_name = _("Billet")
        verbose_name_plural = _("Billets")
        indexes = [
            models.Index(fields=["status", "purchase_date"]),
        ]

    def generate_ticket_number(self):
        """Génère un numéro de billet unique."""
        return f"TIK-{uuid.uuid4().hex[:8].upper()}"

    def clean(self):
        """Validation personnalisée pour le billet."""
        if (
            self.status == self.StatusChoices.CONFIRMED
            and not self.event.is_available()
        ):
            raise ValidationError(
                _("Cet événement n'est pas disponible pour la réservation.")
            )

    def save(self, *args, **kwargs):
        """Sauvegarde personnalisée avec gestion des places et numéro de billet."""
        if not self.pk:
            if not self.ticket_number:
                self.ticket_number = self.generate_ticket_number()

            if self.status == self.StatusChoices.CONFIRMED:
                if self.event.seats_available <= 0:
                    raise ValidationError(
                        _("Plus de places disponibles pour cet événement.")
                    )
                self.total_price = self.event.price

        super().save(*args, **kwargs)

        if self.status == self.StatusChoices.CONFIRMED:
            self.event.save()  # Met à jour les places disponibles

    def __str__(self):
        return f"Billet {self.ticket_number} - {self.event.title}"
