from rest_framework import serializers

from api.model.user_model import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'cpf', 'address', 'phone', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
            }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'email', 'cpf', 'address', 'phone', 'created_at', 'updated_at')
