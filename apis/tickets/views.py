from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.tickets.serializers import TicketSerializer
from apps.tickets.models import Ticket


class TicketListView(APIView):
    """to display ticket"""

    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


class TicketCreateView(APIView):

    "to create a ticket"

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
