from django.contrib import admin
from apps.tickets.models import Ticket


@admin.register (Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_number",
        "event",
        "user",
        "status",
        "purchase_date",
    )
    list_filter = (
        "event",
        "status",
        "purchase_date",
    )
    search_fields = (
        "ticket_number",
        "user_email",
        "event_title",
        "user_username",
    )
    ordering = (
        "purchase_date",
    )
    fieldsets = (
          ("tickets details", {
              "fields" : (
                  "user",
                  "event",
                  "status",

              )
          } ),
    )
    def get_queryset(self, request):
        """Optimise les requêtes pour les champs liés."""
        queryset = super().get_queryset(request)
        return queryset.select_related("event", "user")