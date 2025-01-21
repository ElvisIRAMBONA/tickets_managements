from django.contrib import admin
from apps.halls.models import Halls


@admin.register(Halls)
class HallsAdmin(admin.ModelAdmin):
    model = Halls
    list_display = ("name", "location", "capacity", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "location")
    ordering = ("name",)

    fieldsets = (
        (None, {
            "fields": ("name", "image", "capacity", "location", "is_active")
        }),
    )

    def get_queryset(self, request):
        """Customize the queryset to include related events."""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("events")

    def get_upcoming_events(self, obj):
        """Custom display for upcoming events related to the hall."""
        events = obj.get_upcoming_events()
        if events.exists():
            return ", ".join(event.title for event in events)
        return "No upcoming events"

    get_upcoming_events.short_description = "Upcoming Events"
