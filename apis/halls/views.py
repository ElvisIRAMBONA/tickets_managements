from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apis.events.views import BaseApi
from apis.halls.serializers import HallSerializer
from apps.halls.models import Halls


class HallListView(BaseApi):
    """display list of halls"""

    def get(self, request):
        halls = Halls.objects.all()
        serializer = HallSerializer(halls, many=True)
        return Response(serializer.data)


class HallCreateView(BaseApi):
    "create hall"

    def post(self, request):
        serializer = HallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
