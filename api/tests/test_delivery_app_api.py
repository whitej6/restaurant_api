from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.models import DeliveryApp
from api.serializers import DeliveryAppSerializer


DELIVERYAPP_URL = reverse('api:deliveryapp-list')


class PublicDeliveryAppAPITests(TestCase):
    """

    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """

        """
        r = self.client.get(DELIVERYAPP_URL)

        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDeliveryAppAPITests(TestCase):
    """

    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'noreply@ntc.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_delivery_apps(self):
        """

        """
        DeliveryApp.objects.create(name='Foo')
        DeliveryApp.objects.create(name='Bar')

        r = self.client.get(DELIVERYAPP_URL)

        delivery_apps = DeliveryApp.objects.all().order_by('-name')
        serializer = DeliveryAppSerializer(delivery_apps, many=True)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, serializer.data)

    def test_delivery_apps_limited_to_user(self):
        """
        Test that delivery_apps are limited to authenticated user
        """
        DeliveryApp.objects.create(name='Baz')
        DeliveryApp.objects.create(name='Foo')

        r = self.client.get(DELIVERYAPP_URL)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

    def test_create_delivery_app_successful(self):
        """

        """

        payload = {'name': 'foo'}
        self.client.post(DELIVERYAPP_URL, payload)

        exists = DeliveryApp.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_delivery_app_invalid(self):
        """

        """
        payload = {'name': ''}
        r = self.client.post(DELIVERYAPP_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
