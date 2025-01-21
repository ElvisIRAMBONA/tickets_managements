# apps/tickets/urls.py
from django.urls import path

from .views import TicketCreateView,TicketManagementView

urlpatterns = [

    path("create/", TicketCreateView.as_view(), name="create"),
    path("tickets_manage/", TicketManagementView.as_view(), name="ticket-list-create"),
    path("tickets_manage/<int:pk>/", TicketManagementView.as_view(), name="ticket-detail"),
]