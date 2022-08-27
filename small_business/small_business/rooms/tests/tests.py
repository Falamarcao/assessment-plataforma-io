from os import environ
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from django.core.management import call_command
from django.db.models import ProtectedError

from ...users.management.commands import create_groups
from .utils import json_to_file

# set true to record json files on tests/results directory
record_json = int(environ.get("DEBUG", default=0))


class RoomAPITest(APITestCase):
    fixtures = ['customers.json', 'staff.json', 'rooms.json', 'events.json']

    @classmethod
    def setUpClass(cls):
        call_command(create_groups.Command(), verbosity=0)
        super().setUpClass()

        cls.client = APIClient(SESSION_ID='1')
        cls.api_url = reverse('rooms-list')
        cls.api_detail = 'rooms-detail'
        cls.api_detail2 = 'events-detail'

        cls.staff_username = 'staff'
        cls.password = 'password'

    def test_business_create_room(self):
        """
        The business can create a room with M capacity.
        """

        # LOGIN
        self.assertTrue(
            self.client.login(username=self.staff_username, password=self.password),
            msg=f'Login as {self.staff_username}'
        )

        data = {
            'name': 'Room - test_business_create_room',
            'capacity': 10
        }
        response = self.client.post(self.api_url, data, format='json')

        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        finally:
            if record_json:
                json_to_file(response.data, 'test_business_create_room')

    def test_business_delete_room(self):
        """
        The business can delete a room if said room does not have any events.
        """

        # LOGIN
        self.assertTrue(
            self.client.login(username=self.staff_username, password=self.password),
            msg=f'Login as {self.staff_username}'
        )

        data = {'pk': 1}

        # Trying to delete a room
        msg = "Cannot delete some instances of model \'Room\' " \
              "because they are referenced through protected foreign keys: \'Event.room\'."
        try:
            with self.assertRaisesMessage(ProtectedError, msg):
                self.client.delete(reverse(self.api_detail, kwargs=data), format='json')

            # Deleting events
            response = self.client.delete(reverse(self.api_detail2, kwargs={'pk': 1}), format='json')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            response = self.client.delete(reverse(self.api_detail2, kwargs={'pk': 5}), format='json')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            # Trying again to delete a room after deleting related events
            response = self.client.delete(reverse(self.api_detail, kwargs=data), format='json')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        finally:
            if record_json:
                json_to_file(response.data, 'test_business_delete_room')
