from django.test import TestCase
from django.contrib.auth import get_user_model

from api import models


def sample_user(email='noreply@ntc.com', password='password'):
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    """

    """

    def test_create_user_with_email_successful(self):
        """

        """

        email = 'noreply@ntc.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """

        """

        email = 'noreply@NTC.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='password'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """

        """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """

        """

        user = get_user_model().objects.create_superuser(
            'noreply@ntc.com',
            'foo'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_delivery_app_str(self):
        """

        """

        delivery_app = models.DeliveryApp.objects.create(
            name='Door Dash'
        )
        self.assertEqual('door-dash', delivery_app.slug)

    def test_restaurant_str(self):
        """

        """
        delivery_app = models.DeliveryApp.objects.create(
            name='Door Dash'
        )
        restaurant = models.Restaurant.objects.create(
            name='Foobar Bar',
            address_line_1='123 Main St',
            address_line_2='Suite 123',
            city='Houston',
            state='Tx',
            zip_code='77001',
            phonenumber='111-222-3333',
            hours='Mon-Sun 8:00am-5:00pm',
            dine_in=False,
            take_out=True,
            curbside=True,
            delivery=True,
            website='https://FoobarBar.com',
            user=sample_user()
        )
        restaurant.delivery_apps.add(delivery_app)
        self.assertEqual(str(restaurant), restaurant.name)
