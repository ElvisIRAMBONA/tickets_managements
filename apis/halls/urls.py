# apps/halls/urls.py
from django.urls import path

from .views import HallCreateView, HallListView

urlpatterns = [
    path("show/", HallListView.as_view(), name="hall_list"),
    path("create/", HallCreateView.as_view(), name="create"),
]
