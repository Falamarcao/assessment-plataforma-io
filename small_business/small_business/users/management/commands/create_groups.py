from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
from django.core.management.base import BaseCommand

from ....events.models import Event
from ....rooms.models import Room


class Command(BaseCommand):
    help = 'Creates customer group for users and add permissions'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.groups = [
            {
                "name": "staff",
                "allowed_actions": [
                    "add_room",
                    "change_room",
                    "delete_room",
                    "view_room",

                    "add_event",
                    "change_event",
                    "delete_event",
                    "view_event",
                ]
            },
            {
                "name": "customers",
                "allowed_actions": [
                    "add_event",
                    "delete_event"
                ]
            },
        ]

    @property
    def permissions(self):
        content_type = ContentType.objects.get_for_model(Room)
        room_permissions = Permission.objects.filter(content_type=content_type)

        content_type = ContentType.objects.get_for_model(Event)
        event_permissions = Permission.objects.filter(content_type=content_type)

        return room_permissions.union(event_permissions)

    def add_permissions_to_group(self, group, allowed_actions):
        for permission in self.permissions:
            if permission.codename in allowed_actions:
                group.permissions.add(permission)
                print(f"Permission {permission.codename} add to Group {str(group)}")

    def handle(self, *args, **options):
        for group in self.groups:
            new_group, created = Group.objects.get_or_create(name=group['name'])
            if created:
                print(f"Group {str(new_group)} was created.")

                if group.get('allowed_actions'):
                    self.add_permissions_to_group(new_group, group['allowed_actions'])

            else:
                print(f"Group {str(new_group)} already exists.")
