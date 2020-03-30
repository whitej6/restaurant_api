from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('delivery_app', views.DeliveryAppViewSet)
router.register('restaurant', views.RestaurantViewSet)
router.register('user', views.UserViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls))
]
