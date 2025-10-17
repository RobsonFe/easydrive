from rest_framework import serializers
from rent.models import Rental
from client.serializers import ClientSerializer
from vehicle.serializers import VehicleSerializer


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = "__all__"  # Serializa todos os campos do modelo Rental


class RentListSerializer(serializers.ModelSerializer):
    client_data = ClientSerializer(source="client")
    vehicle_data = VehicleSerializer(source="vehicle")

    class Meta:
        model = Rental
        fields = ["id", "start_date", "end_date", "client_data", "vehicle_data"]


class RentServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ["id", "end_date", "returned", "client", "vehicle"]
        extra_kwargs = {
            "client": {"read_only": True},
            "vehicle": {"read_only": True},
        }
