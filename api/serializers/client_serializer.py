from dataclasses import field
from rest_framework import serializers
from api import model
from api.model.client_model import Client
from api.model.rent_model import Rental
from api.model.vehicle_model import Vehicle
from api.serializers.user_serializer import UserSerializer


class ClientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'user', 'total_rentals']

class ClientSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user')  # Define o campo user_data como um serializer aninhado ao User

    class Meta:
        model = Client
        fields = ['id', 'total_rentals', 'user_data']  # Inclui o campo user_data
        
class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields =  '__all__'  # Serializa todos os campos do modelo Rental
        


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'year', 'is_available']  
        extra_kwargs = {'is_available': {'read_only': True}}

class RentListSerializer(serializers.ModelSerializer):
    client_data = ClientSerializer(source = 'client')
    vehicle_data = VehicleSerializer(source = 'vehicle')
    class Meta:
        model = Rental
        fields =  ['id','start_date', 'end_date', 'client_data', 'vehicle_data',]