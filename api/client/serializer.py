from rest_framework import serializers
from api.client.models import Client
from api.accounts.serializer import UserSerializer


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer para serialização de cliente com dados do usuário aninhados.
    
    Attributes:
        user_data: Dados completos do usuário associado ao cliente.
    """
    user_data = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'total_rentals', 'user_data']
        read_only_fields = ['id', 'total_rentals']


class ClientDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer para detalhes completos do cliente.
    
    Inclui o ID do usuário e dados completos do usuário aninhados.
    
    Attributes:
        client_data: Dados completos do usuário associado ao cliente.
    """
    client_data = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'user', 'total_rentals', 'client_data']
        read_only_fields = ['id', 'total_rentals']
