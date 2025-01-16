# apps/tickets/urls.py
from django.urls import path

from .views import TicketListView

urlpatterns = [
    path("show/", TicketListView.as_view(), name="ticket_list"),
]
