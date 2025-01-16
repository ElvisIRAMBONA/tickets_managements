# apps/tickets/urls.py
from django.urls import path

from .views import TicketCreateView, TicketListView

urlpatterns = [
    path("show/", TicketListView.as_view(), name="ticket_list"),
    path("create/", TicketCreateView.as_view(), name="create"),
]
