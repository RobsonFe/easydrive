
from rest_framework import serializers
from client.models import Client
from vehicle.models import TypeVehicle
from api.accounts.serializer import UserSerializer


class ClientDetailsSerializer(serializers.ModelSerializer):
    client_data = UserSerializer(source='user')

    class Meta:
        model = Client
        fields = ['id', 'user', 'total_rentals', 'client_data']


    user_data = UserSerializer(source='user')

    class Meta:
        fields = ['id', 'total_rentals', 'user_data']


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    type_vehicle = serializers.ChoiceField(
        choices=TypeVehicle.choices, default=TypeVehicle.CAR)

    class Meta:
        fields = ['id', 'brand', 'model', 'year', 'quantity',
                  'type_vehicle', 'description', 'is_available']
        extra_kwargs = {'is_available': {'read_only': True}}


class RentListSerializer(serializers.ModelSerializer):
    client_data = ClientDetailsSerializer(source='client')
    vehicle_data = VehicleSerializer(source='vehicle')

    class Meta:
        fields = ['id', 'start_date', 'end_date',
                  'client_data', 'vehicle_data']


class RentServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'end_date', 'returned', 'client', 'vehicle']
        extra_kwargs = {
            'client': {'read_only': True},
            'vehicle': {'read_only': True},
        }
