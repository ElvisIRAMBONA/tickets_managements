# apis/users/urls.py
from django.urls import path

from .views import UserCreateView, UserListView,LoginView


urlpatterns = [
    path("show/", UserListView.as_view(), name="show"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/",LoginView.as_view(),name='login'),
]
