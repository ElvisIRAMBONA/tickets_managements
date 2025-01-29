from elasticsearch.helpers import bulk
from django.core.management.base import BaseCommand
from apps.events.models import Event
from apis.events.documents import EventDocument

class Command(BaseCommand):
    help = "Index all events in Elasticsearch."

    def handle(self, *args, **kwargs):
        events = Event.objects.all()
        actions = []
        for event in events:
            doc = EventDocument.from_django(event)
            action = doc.to_dict(include_meta=True)  # Convert to dict, include meta for Elasticsearch
            actions.append(action)

        success, failed = bulk(EventDocument._doc_type.client, actions)
        if success:
            self.stdout.write(self.style.SUCCESS(f"Successfully indexed {success} events in Elasticsearch."))
        if failed:
            self.stdout.write(self.style.ERROR(f"Failed to index {failed} events."))
