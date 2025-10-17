from rest_framework import serializers
from client.models import Client
from account.serializers import UserSerializer


class ClientDetailsSerializer(serializers.ModelSerializer):
    client_data = UserSerializer(source="user")

    class Meta:
        model = Client
        fields = ["id", "user", "total_rentals", "client_data"]


class ClientSerializer(serializers.ModelSerializer):
    # Define o campo user_data como um serializer aninhado ao User
    user_data = UserSerializer(source="user")

    class Meta:
        model = Client
        # Inclui o campo user_data
        fields = ["id", "total_rentals", "user_data"]
