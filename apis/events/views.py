from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from silk.profiling.profiler import silk_profile
from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.tickets.models import Ticket
from django.utils.timezone import now
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apis.tickets.views import BaseApi



class EventListView(BaseApi):

    @silk_profile(name="events profiling - GET")
    def get(self, request):

        events = Event.objects.select_related('user', 'hall').prefetch_related('tickets').all()

        #serialization of events and tickets associated
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data)

class EventCreateView(BaseApi):
    @silk_profile(name="events profiling - POST")
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpcomingEventsView(BaseApi):

    def get(self, request, *args, **kwargs):

        current_time = now()

        # Filter on th upcoming event
        upcoming_events = Event.objects.filter(end_date__gt=current_time)

        # data serialization
        serializer = EventSerializer(upcoming_events, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

