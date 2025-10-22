# apis/events/documents
from apps.events.models import Event
from elasticsearch_dsl import Document, Text, Date, Keyword, Integer
from elasticsearch_dsl.connections import connections
from apps.events.models import Event




# Connexion à Elasticsearch
connections.create_connection(
    hosts=["http://localhost:9200"],
    timeout=30,  # Timeout de 30 secondes
    max_retries=10,  # Nombre maximal de tentatives de reconnexion
    retry_on_timeout=True  # Réessayer en cas de timeout
)

class EventDocument(Document):
    title = Text()
    description = Text()
    date = Date(format='yyyy-MM-dd')
    end_date = Date()
    price = Integer()
    status =Keyword()

    class Index:
        name = 'events'  # Name of index elasticsearch

    def save(self, **kwargs):
        return super().save(**kwargs)

    @classmethod
    def from_django(cls, event):
        """Converti django object `Event` into document Elasticsearch."""
        return cls(
            meta={'id': event.id},
            title=event.title,
            description=event.description,
            date=event.date,
            end_date=event.end_date,
            price=event.price,
            status=event.status,
        )
