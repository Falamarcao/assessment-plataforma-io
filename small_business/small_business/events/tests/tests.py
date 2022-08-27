from os import environ
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from django.core.management import call_command

from ...users.management.commands import create_groups
from .utils import json_to_file

# set true to record json files on tests/results directory
record_json = int(environ.get("DEBUG", default=0))


class EventAPITest(APITestCase):
    fixtures = ['customers.json', 'staff.json', 'rooms.json', 'events.json']

    @classmethod
    def setUpClass(cls):
        call_command(create_groups.Command(), verbosity=0)
        super().setUpClass()

        cls.client = APIClient(SESSION_ID='1')
        cls.api_url = reverse('events-list')

        cls.customer_username = 'Paul McCartney'
        cls.staff_username = 'staff'
        cls.password = 'password'

    def test_business_create_events(self):
        """
        The business can create events for every room.
        """

        # LOGIN
        self.assertTrue(
            self.client.login(username=self.staff_username, password=self.password),
            msg=f'Login as {self.staff_username}'
        )

        data = {
            'name': 'Gaming with your boos',
            'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. '
                           'Aenean commodo ligula eget dolor. Aenean massa. '
                           'Cum sociis natoque penatibus et ma',
            'event_type': 'private',
            'start_at': '2022-01-01T12:20:30+03:00',
            'end_at': '2022-01-01T12:20:30+03:00',
            'room': 2,
            'event_participants': [2, 3, 4]
        }
        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        if record_json:
            json_to_file(response.data, 'test_business_create_events')

    # def test_customer_list_public_events(self):
    #     """
    #     A customer can see all the available public events.
    #     """
    #
    #     # LOGIN
    #     self.assertTrue(
    #         self.client.login(username=self.customer_username, password=self.password),
    #         msg=f'Login as {self.staff_username}'
    #     )
    #
    #     data = {
    #         'limit': 1,
    #         'p': 1
    #     }
    #     response = self.client.get(self.api_url, data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['results']), 1)
    #
    #     if record_json:
    #         json_to_file(response.data, 'test_customer_list_public_events_(limit 1 p1)')
    #
    #     data = {
    #         'limit': 100,
    #         'p': 1
    #     }
    #     response = self.client.get(self.api_url, data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['results']), 2)
    #
    #     if record_json:
    #         json_to_file(response.data, 'test_customer_list_public_events_(limit 100 p1)')
    #
    # def test_customer_list_public_events_by_date_range(self):
    #     """
    #     A customer can see all the available public events.
    #     """
    #
    #     # LOGIN
    #     self.assertTrue(
    #         self.client.login(username=self.customer_username, password=self.password),
    #         msg=f'Login as {self.staff_username}'
    #     )
    #
    #     data = {
    #         'start_at': '2021-02-01',
    #         'end_at': '2021-02-01'
    #     }
    #     response = self.client.get(self.api_url, data, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['results']), 1)
    #
    #     if record_json:
    #         json_to_file(response.data, 'test_customer_list_public_events_by_date_range')


