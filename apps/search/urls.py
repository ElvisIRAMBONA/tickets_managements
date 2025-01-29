from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_event, name='search_event'),
]
