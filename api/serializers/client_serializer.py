from dataclasses import field
from rest_framework import serializers
from api import model
from api.model.client_model import Client
from api.model.rent_model import Rental
from api.model.vehicle_model import TypeVehicle, Vehicle
from api.serializers.user_serializer import UserSerializer


class ClientDetailsSerializer(serializers.ModelSerializer):
    client_data = UserSerializer(source='user')

    class Meta:
        model = Client
        fields = ['id', 'user', 'total_rentals', 'client_data']


class ClientSerializer(serializers.ModelSerializer):
    # Define o campo user_data como um serializer aninhado ao User
    user_data = UserSerializer(source='user')

    class Meta:
        model = Client
        # Inclui o campo user_data
        fields = ['id', 'total_rentals', 'user_data']


class RentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='id', read_only=True)

    class Meta:
        model = Rental
        fields = '__all__'  # Serializa todos os campos do modelo Rental


class VehicleSerializer(serializers.ModelSerializer):
    type_vehicle = serializers.ChoiceField(
        choices=TypeVehicle.choices, default=TypeVehicle.CAR)

    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'year', 'quantity',
                  'type_vehicle', 'description', 'is_available']
        extra_kwargs = {'is_available': {'read_only': True}}


class RentListSerializer(serializers.ModelSerializer):
    client_data = ClientSerializer(source='client')
    vehicle_data = VehicleSerializer(source='vehicle')

    class Meta:
        model = Rental
        fields = ['id', 'start_date', 'end_date',
                  'client_data', 'vehicle_data']


class RentServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'end_date', 'returned', 'client', 'vehicle']
        extra_kwargs = {
            'client': {'read_only': True},
            'vehicle': {'read_only': True},
        }
