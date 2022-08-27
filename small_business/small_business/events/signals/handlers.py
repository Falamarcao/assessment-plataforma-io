from django.core.validators import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from ..models import Event


@receiver(m2m_changed, sender=Event.event_participants.through)
def set_and_check_occupancy(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        instance.save()

