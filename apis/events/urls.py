# apps/events/urls.py
from django.urls import path
from .views import EventListView, EventCreateView,UpcomingEventsView ,SearchEventsAPIView,EventUpdateView,EventDeleteView

urlpatterns = [
    path("show/", EventListView.as_view(), name="list_event"),
    # path("create/",EventCreateView.as_view(),name="create"),
    path("upcoming-events/", UpcomingEventsView.as_view(), name="upcoming-events"),
    path("events/create/", EventCreateView.as_view(), name="event_create"),
    path('search/', SearchEventsAPIView.as_view(), name='search_events'),
    path('events/<int:event_id>/update/',EventUpdateView.as_view(), name='update_event'),
    path('events/<int:event_id>/delete/',EventDeleteView.as_view(), name='delete_event'),

]