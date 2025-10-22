# apis/tickets/urls.py
from django.urls import path

from .views import TicketCreateView,TicketManagementView

app_name = 'tickets'

urlpatterns = [
    path("create/", TicketCreateView.as_view(), name="create"),
    path("tickets_manage/", TicketManagementView.as_view(), name="ticket-list-create"),
    path("tickets_manage/<int:pk>/", TicketManagementView.as_view(), name="ticket-detail"),
    path('tickets/', TicketCreateView.as_view(), name='ticket-create'),
    path("tickets/create/", TicketCreateView.as_view(), name="ticket-create"),
    path('tickets/<int:pk>/', TicketManagementView.as_view(), name='ticket-management'),
]


