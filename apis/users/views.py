from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import CustomUser

from .serializers import UserSerializer


class UserListView(APIView):
    """display users"""

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserCreateView(APIView):
    "create user"

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
