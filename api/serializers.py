from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DeliveryApp, Restaurant
from .fields import DeliveryAppField


class UserSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """

        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """

        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class DeliveryAppSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = DeliveryApp
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


class RestaurantSerializer(serializers.ModelSerializer):
    """

    """
    user = UserSerializer(required=False)
    delivery_apps = DeliveryAppField(many=True)
    date_modified = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ['id']

    def get_date_modified(self, obj):
        return obj.date_modified.strftime('%m-%d-%Y %H:%M UTC')
