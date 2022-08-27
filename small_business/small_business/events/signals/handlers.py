from django.core.validators import ValidationError
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from ..models import Event

from rest_framework.response import Response
from rest_framework import status


@receiver(m2m_changed, sender=Event.event_participants.through)
def set_occupancy(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        if instance.id:
            instance.occupancy = instance.event_participants.count()
            instance.save(update_fields=['occupancy'])


@receiver(pre_save, sender=Event)
def check_occupancy(sender, instance, *args, **kwargs):
    if instance.event_participants.count() > instance.room.capacity:
        return Response("Room out of capacity.", status.HTTP_400_BAD_REQUEST)
