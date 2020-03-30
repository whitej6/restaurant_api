from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Restaurant, DeliveryApp
from api.serializers import RestaurantSerializer


RESTAURANT_URL = reverse('api:restaurant-list')
RESTAURANT_PAYLOAD = {
    "delivery_apps": [
        "DoorDash"
    ],
    "name": "Foobaz Bar",
    "address_line_1": "123 Main St",
    "address_line_2": "Suite 100",
    "city": "The Woodlands",
    "state": "TX",
    "zip_code": "77380",
    "phonenumber": "(123) 456-7890",
    "hours": "24/7",
    "dine_in": False,
    "take_out": True,
    "drive_thru": False,
    "curbside": True,
    "delivery": False,
    "website": "https://foobaz.bar/",
    "email": "foo@foobaz.bar",
    "notes": "Offering the best foo since 2020"
}


class PublicRestaurantAPITests(TestCase):
    """

    """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """

        """
        r = self.client.get(RESTAURANT_URL)

        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRestaurantAPITests(TestCase):
    """

    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'noreply@ntc.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.delivery_app = DeliveryApp.objects.create(name='FooDash')
        self.restaurant = Restaurant.objects.create(
            user=self.user,
            name="Foobaz Bar",
            address_line_1="123 Main St",
            address_line_2="Suite 100",
            city="The Woodlands",
            state="TX",
            zip_code="77380",
            phonenumber="(123) 456-7890",
            hours="24/7",
            dine_in=False,
            take_out=True,
            drive_thru=False,
            curbside=True,
            delivery=False,
            website="https://foobaz.bar/",
            email="foo@foobaz.bar",
            notes="Offering the best foo since 2020"
        )
        self.restaurant.delivery_apps.add(self.delivery_app)

    def test_retrieve_restaurants(self):
        """

        """

        r = self.client.get(RESTAURANT_URL)

        restaurants = Restaurant.objects.all().order_by('-name')
        serializer = RestaurantSerializer(restaurants, many=True)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data, serializer.data)

    def test_create_restaurant_successful(self):
        """

        """

        self.client.post(RESTAURANT_URL, RESTAURANT_PAYLOAD)

        exists = Restaurant.objects.filter(
            name=RESTAURANT_PAYLOAD['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_restaurant_invalid(self):
        """

        """
        payload = {'name': ''}
        r = self.client.post(RESTAURANT_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
