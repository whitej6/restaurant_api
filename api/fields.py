from django.utils.text import slugify
from rest_framework import serializers

from .models import DeliveryApp


class DeliveryAppField(serializers.RelatedField):
    """

    """
    queryset = DeliveryApp.objects.all()

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        try:
            app = DeliveryApp.objects.get(slug=slugify(data))
        except DeliveryApp.DoesNotExist:
            app = DeliveryApp.objects.create(name=data)
        return app.pk
