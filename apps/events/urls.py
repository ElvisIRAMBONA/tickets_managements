# apps/events/urls.py
from django.urls import path

from .views import EventListView

urlpatterns = [
    path("show/", EventListView.as_view(), name="list_event"),
]
