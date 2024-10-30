from rest_framework import serializers
from api.model.client_model import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'user', 'total_rentals']
