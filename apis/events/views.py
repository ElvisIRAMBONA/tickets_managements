from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from silk.profiling.profiler import silk_profile
from apps.events.models import Event
from apps.events.serializers import EventSerializer
from django.utils.timezone import now
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apis.tickets.views import BaseApi
from elasticsearch_dsl import Q
from .documents import EventDocument
from django.core.cache import cache

class EventListView(BaseApi):
    CACHE_KEY = "all_events"
    CACHE_TIMEOUT = 60 * 5  # 5 minutes and then be removed

    @silk_profile(name="events profiling - GET")
    def get(self, request):
        # Vérifier si les événements sont déjà stockés dans le cache
        events = cache.get(self.CACHE_KEY)

        if not events:
            print("Fetching events from database...")
            # Récupérer les événements depuis la base de données
            events = Event.objects.select_related('user', 'hall').prefetch_related('tickets').all()
            serializer = EventSerializer(events, many=True)
            events = serializer.data

            # Stocker les résultats dans le cache pour la prochaine fois
            cache.set(self.CACHE_KEY, events, timeout=self.CACHE_TIMEOUT)
            print("Events stored in cache.")
        else:
            print("Fetching events from cache...")

        return Response(events)

class EventCreateView(BaseApi):
    @silk_profile(name="events profiling - POST")
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Supprimer le cache des événements lorsque un nouvel événement est créé
            cache.delete(EventListView.CACHE_KEY)
            print("Cache deleted after event creation.")

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventUpdateView(APIView):
    def put(self, request, event_id):
        try:
            # Trouver l'événement à mettre à jour
            event = Event.objects.get(id=event_id)
            serializer = EventSerializer(event, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()

                # Supprimer le cache des événements
                cache.delete(EventListView.CACHE_KEY)
                cache.delete(UpcomingEventsView.CACHE_KEY)  # Si applicable pour les événements à venir

                # Optionnel : Recréer le cache avec les données mises à jour
                updated_event = Event.objects.select_related('user', 'hall').prefetch_related('tickets').all()
                updated_serializer = EventSerializer(updated_event, many=True)
                cache.set(EventListView.CACHE_KEY, updated_serializer.data, timeout=60 * 5)

                print(f"Event with ID {event_id} updated successfully.")
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            print(f"Event with ID {event_id} not found.")
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

class EventDeleteView(APIView):
    def delete(self, request, event_id):
        try:
            # Trouver l'événement à supprimer
            event = Event.objects.get(id=event_id)
            event.delete()

            # Supprimer le cache des événements
            cache.delete(EventListView.CACHE_KEY)
            cache.delete(UpcomingEventsView.CACHE_KEY)  # Si applicable

            print(f"Event with ID {event_id} deleted successfully.")
            return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            print(f"Event with ID {event_id} not found.")
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

class UpcomingEventsView(BaseApi):
    CACHE_KEY = "upcoming_events"
    CACHE_TIMEOUT = 60 * 5  # 5 minutes

    def get(self, request, *args, **kwargs):
        current_time = now()

        # Vérifier si les événements à venir sont dans le cache
        upcoming_events = cache.get(self.CACHE_KEY)

        if not upcoming_events:
            print("Fetching upcoming events from database...")
            # Récupérer les événements à venir depuis la base de données
            upcoming_events = Event.objects.filter(end_date__gt=current_time)
            serializer = EventSerializer(upcoming_events, many=True)
            upcoming_events = serializer.data

            # Stocker les résultats dans le cache pour la prochaine fois
            cache.set(self.CACHE_KEY, upcoming_events, timeout=self.CACHE_TIMEOUT)
            print("Upcoming events stored in cache.")
        else:
            print("Fetching upcoming events from cache...")

        return Response(upcoming_events, status=status.HTTP_200_OK)

class SearchEventsAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')  # Mot-clé principal
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        status = request.GET.get('status')

        # Clé de cache unique pour la recherche
        cache_key = f"search_events:{query}:{price_min}:{price_max}:{status}"
        cached_results = cache.get(cache_key)

        if cached_results:
            print("Fetching search results from cache...")
            return Response(cached_results)

        print("Fetching search results from Elasticsearch...")
        # Construire une requête Elasticsearch
        search = EventDocument.search()
        if query:
            search = search.query("multi_match", query=query, fields=["title", "description"])
        if price_min:
            search = search.filter("range", price={"gte": price_min})
        if price_max:
            search = search.filter("range", price={"lte": price_max})
        if status:
            search = search.filter("term", status=status)

        try:
            # Exécuter la recherche dans Elasticsearch
            results = search.execute()
            data = [
                {
                    "id": hit.meta.id,
                    "title": hit.title,
                    "description": hit.description,
                    "price": hit.price,
                    "status": hit.status,
                }
                for hit in results
            ]

            # Stocker les résultats en cache
            cache.set(cache_key, data, timeout=60 * 5)  # Expire après 5 minutes
            print("Search results stored in cache.")

            return Response(data)
        except Exception as e:
            print(f"Error executing search: {e}")
            return Response({"error": "Search execution failed"}, status=500)
