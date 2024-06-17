import json
import os

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import NetworkLink

# Defining the base directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Determining paths to files with test data
file_path_user = os.path.join(base_dir, 'data_for_tests', 'users.json')
file_path_workplace = os.path.join(base_dir, 'data_for_tests', 'network_links.json')
file_path_reverse = os.path.join(base_dir, 'data_for_tests', 'reverse.json')

# Loading user test data
with open(file_path_user) as f:
    test_data = json.load(f)
    data_test_user_admin_is_active_1 = test_data['data_test_user_admin_is_active_1']
    data_test_user_admin_is_active_2 = test_data['data_test_user_admin_is_active_2']


# Loading application test data
with open(file_path_workplace) as f:
    test_data = json.load(f)
    data_test_network_link_1 = test_data['data_test_network_link_1']
    data_test_network_link_2 = test_data['data_test_network_link_2']
    data_test_network_link_3 = test_data['data_test_network_link_3']

    data_test_network_lind_exception_1 = test_data['data_test_network_lind_exception_1']


# Loading the path to compose the url
with open(file_path_reverse) as f:
    d_r = json.load(f)  # data for reverse
    url_create = f'{d_r["APP"]["NL"]["name"]}:{d_r['CRUD']['POST']}'
    url_get = f'{d_r["APP"]["NL"]["name"]}:{d_r["CRUD"]["GET"]}'
    url_update = f'{d_r["APP"]["NL"]["name"]}:{d_r["CRUD"]["PUT"]}'
    url_delete = f'{d_r["APP"]["NL"]["name"]}:{d_r["CRUD"]["DELETE"]}'
    url_list = f'{d_r["APP"]["NL"]["name"]}:{d_r["CRUD"]["LIST"]}'


def tear_down() -> None:
    """Clear all tables associated with tests."""

    NetworkLink.objects.all().delete()
    User.objects.all().delete()


class NetworkLinkUserWithAdminAndAuthenticationIsActiveTestCase(APITestCase):
    """
    Tests of CRUD operations in the NetworkLinks application with a user with admin status
    with passed authentication and active status.
    """

    def setUp(self) -> None:
        """Create test data."""

        # Clear all tables associated with tests
        tear_down()

        # Create users for tests with admin status with passed authentication and active status
        self.user_admin_1 = User.objects.create(
            email=data_test_user_admin_is_active_1['email'],
        )
        self.user_admin_1.set_password(data_test_user_admin_is_active_1['password'])
        self.user_admin_1.save()
        self.client.force_authenticate(user=self.user_admin_1)

        # Create NetworkLink model instances for tests
        self.network_link_2 = NetworkLink.objects.create(
            **data_test_network_link_2
        )
        self.network_link_3 = NetworkLink.objects.create(
            **data_test_network_link_3
        )

    def test_create_network_link_with_validation_error(self) -> None:
        """Testing NetworkLink creation with validation error."""

        # Trying to instantiate a NetworkLink model with a third layer
        response = self.client.post(
            reverse(url_create),
            data=data_test_network_lind_exception_1
        )

        # Check request status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_network_link(self):
        """Testing NetworkLink Reception."""

        # Get a NetworkLink model instance
        response = self.client.get(reverse(url_get, args=[self.network_link_2.id]))

        # Check request status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check data
        self.assertEqual(response.data['name'], self.network_link_2.name)

    def test_list_network_link(self):
        """Testing NetworkLink List Retrieval."""

        # Get a NetworkLink model instance
        response = self.client.get(reverse(url_list))

        # Check request status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check data
        self.assertEqual(len(response.data['results']), 2)

        # Check if there is a link to the next page
        self.assertIsNone(response.data['next'])

    def test_delete_network_link(self):
        """Testing NetworkLink removal."""

        # Delete a NetworkLink model instance
        response = self.client.delete(reverse(url_delete, args=[self.network_link_2.id]))

        # Check request status
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check the existence of an object
        self.assertFalse(NetworkLink.objects.filter(
            name=data_test_network_link_2['name']).exists()
        )
