from django.db.models import Model, CharField, PositiveIntegerField


class Room(Model):
    name = CharField(max_length=140, blank=True, null=False)
    capacity = PositiveIntegerField(default=0, blank=False, null=False)  # REQ1: There are N rooms with M capacity.

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"Room {self.pk}"
        super(Room, self).save(*args, **kwargs)
