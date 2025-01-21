from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from apis.tickets.serializers import TicketSerializer
from apps.tickets.models import Ticket
from rest_framework_simplejwt.authentication import JWTAuthentication


class BaseApi(APIView):
     authentication_classes= [JWTAuthentication]
     permission_classes = [IsAuthenticated]


class TicketCreateView(APIView):
    "to create a ticket"
    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketManagementView(BaseApi):
    """View to manage tickets: create, update, and retrieve."""
    def get(self, request, pk=None, *args, **kwargs):
        """Handle ticket retrieval."""
        if pk:
            # Retrieve a specific ticket
            try:
                ticket = Ticket.objects.get(pk=pk, user=request.user)
            except Ticket.DoesNotExist:
                return Response(
                    {"error": "Ticket not found or unauthorized access"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Retrieve all tickets for the authenticated user
        tickets = Ticket.objects.filter(user=request.user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Handle ticket creation."""
        serializer = TicketSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            ticket = serializer.save()
            return Response(
                {"message": "Ticket created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        """Handle ticket full update."""
        try:
            ticket = Ticket.objects.get(pk=pk, user=request.user)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found or unauthorized access"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TicketSerializer(
            ticket, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Ticket updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        """Handle partial ticket update."""
        try:
            ticket = Ticket.objects.get(pk=pk, user=request.user)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found or unauthorized access"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TicketSerializer(
            ticket, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Ticket updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


