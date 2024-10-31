from rest_framework import serializers
from api.model.client_model import Client
from api.serializers.user_serializer import UserSerializer


class ClientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'user', 'total_rentals']

class ClientSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user')  # Define o campo user_data como um serializer aninhado

    class Meta:
        model = Client
        fields = ['id', 'total_rentals', 'user_data']  # Inclui o campo user_data