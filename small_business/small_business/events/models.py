from django.db.models import (Model, DateTimeField, PositiveIntegerField,
                              CharField, ForeignKey, ManyToManyField,
                              CASCADE, PROTECT)
from django.core.validators import ValidationError
from ..rooms.models import Room
from ..users.models import User


class Event(Model):
    owner = ForeignKey(
        User,
        blank=False,
        null=True,
        on_delete=CASCADE,
        related_name='owner_event'
    )
    name = CharField(max_length=140, blank=False, null=False)
    description = CharField(max_length=140, blank=False, null=False)

    # REQ 2: There are two types of events: public and private.
    EVENT_TYPE_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
    event_type = CharField(max_length=7, choices=EVENT_TYPE_CHOICES)

    start_at = DateTimeField(blank=False, null=False)
    end_at = DateTimeField(blank=False, null=False)

    room = ForeignKey(
        'rooms.Room',
        blank=False,
        null=True,
        on_delete=PROTECT,  # REQ 3: The business can delete a room if said room does not have any events.
        related_name='room_event'
    )

    event_participants = ManyToManyField(
        User,
        blank=False,
        related_name='event_participants'
    )

    occupancy = PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    # DRF > 3.1 doesn't call the model validation methods, so we are not using clean method here.
    def save(self, *args, **kwargs):
        self.room.occupancy = self.event_participants.count()

        if self.occupancy > self.room.capacity:
            raise ValidationError(f"Room full occupancy was reached.")

        super(Event, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('name', 'room', 'start_at',),  # Rule 7 - A customer cannot book a space twice for the same event.
        )
