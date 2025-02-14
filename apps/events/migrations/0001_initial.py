# Generated by Django 5.1.4 on 2025-01-16 09:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("halls", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="title"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                (
                    "capacity",
                    models.PositiveIntegerField(
                        help_text="Number of available seats",
                        null=True,
                        verbose_name="capacity",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Ticket price",
                        max_digits=8,
                        verbose_name="price",
                    ),
                ),
                ("date", models.DateTimeField(verbose_name="start date")),
                ("end_date", models.DateTimeField(verbose_name="end date")),
                (
                    "seats_available",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="available seats"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="event_images/default.jpg",
                        null=True,
                        upload_to="event_images/",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("PUBLISHED", "Published"),
                            ("CANCELLED", "Canceled"),
                            ("SOLD_OUT", "Sold out"),
                            ("FINISHED", "Finished"),
                        ],
                        default="DRAFT",
                        max_length=10,
                        verbose_name="status",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="created at",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "hall",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="halls.halls",
                        verbose_name="hall",
                    ),
                ),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
                "ordering": ["-date"],
            },
        ),
    ]
