# apps/events/urls.py
from django.urls import path

from .views import EventListView, EventCreateView,UpcomingEventsView

urlpatterns = [
    path("show/", EventListView.as_view(), name="list_event"),
    path("create/",EventCreateView.as_view(),name="create"),
    path("upcoming-events/", UpcomingEventsView.as_view(), name="upcoming-events"),
]
