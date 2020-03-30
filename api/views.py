from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import DeliveryApp, Restaurant
from . import serializers


class DeliveryAppViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """

    """
    permission_classes = (IsAuthenticated,)
    queryset = DeliveryApp.objects.all()
    serializer_class = serializers.DeliveryAppSerializer
    authentication_classes = (BasicAuthentication,)


class RestaurantViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """

    """
    permission_classes = (IsAuthenticated,)
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    authentication_classes = (BasicAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    """

    """
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
