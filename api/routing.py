from django.urls import path
from .consumers import VehicleNotificationConsumer

websocket_urlpatterns = [
    path("ws/vehicle/", VehicleNotificationConsumer.as_asgi()),
]
