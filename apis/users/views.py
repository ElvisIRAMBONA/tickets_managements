from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import CustomUser
from .serializers import UserSerializer
from django.contrib.auth import authenticate


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
class LoginView(APIView):
    """View to manage user connection"""

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Vérifier les informations d'identification verify the identification information
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # Generate token (e.g: JWT)
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "full_name": user.get_full_name(),
                            "user_type": user.get_user_type(),
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Ce compte est désactivé."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"error": "Nom d'utilisateur ou mot de passe incorrect."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
