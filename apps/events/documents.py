
from django.contrib.auth.models import User
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Event


@registry.register_document
class EventDocument(Document):
    class Index:
        name = "events"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
    hall = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "name": fields.TextField(),
        "location": fields.TextField(),
    })
    User=fields.ObjectField(properties={
       "id": fields.IntegerField(),
       "username": fields.TextField(),
      "first_name": fields.TextField(),
      "last_name": fields.TextField(),
     "email": fields.TextField(),
    })
    class Django:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "price",
            "date",
            "end_date",
            "capacity",
        ]
