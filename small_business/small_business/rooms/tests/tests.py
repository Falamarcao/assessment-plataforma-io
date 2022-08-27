from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from django.core.management import call_command

from ...users.management.commands import create_groups
from .utils import json_to_file

record_json = False  # set true to record json files on tests/results directory


class RoomAPITest(APITestCase):
    fixtures = ['customers.json', 'staff.json', 'rooms.json', 'events.json']

    @classmethod
    def setUpClass(cls):
        call_command(create_groups.Command(), verbosity=0)
        super().setUpClass()

        cls.client = APIClient(SESSION_ID='1')
        cls.api_url = reverse('rooms-list')
        cls.api_url_events = reverse('events-list')

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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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

        data = {'id': 1}

        # Trying to delete a room
        response = self.client.delete(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Deleting events
        response = self.client.delete(self.api_url_events, {'id': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.api_url_events, {'id': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Trying again to delete a room after deleting related events
        response = self.client.delete(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if record_json:
            json_to_file(response.data, 'test_business_delete_room')
