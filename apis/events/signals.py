from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.events.models import Event
from apis.events.documents import EventDocument

@receiver(post_save, sender=Event)
def index_event(sender, instance, **kwargs):
    """index or update event in Elasticsearch."""
    doc = EventDocument.from_django(instance)
    doc.save()

@receiver(post_delete, sender=Event)
def delete_event_from_index(sender, instance, **kwargs):
    """delete event from_index."""
    try:
        doc = EventDocument.get(id=instance.id)
        doc.delete()
    except Exception:
        pass
