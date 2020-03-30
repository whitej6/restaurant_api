from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('api:user-list')


def create_user(**kwargs):
    """Helper function for creating a user"""
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """

    """

    def setUp(self):
        """

        """
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """

        """

        payload = {
            'email': 'noreply@ntc.com',
            'password': 'password123',
            'name': 'John Smith'
        }
        r = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**r.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', r.data)

    def test_user_exists(self):
        """

        """

        payload = {
            'email': 'noreply@ntc.com',
            'password': 'password123',
            'name': 'John Smith'
        }
        create_user(**payload)

        r = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """

        """

        payload = {
            'email': 'noreply@ntc.com',
            'password': 'pass',
            'name': 'John Smith'
        }
        r = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
