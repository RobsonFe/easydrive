from rest_framework import serializers
from django.conf import settings
from api.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'avatar')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        avatar = data.get('avatar')
        if avatar:
            if avatar.startswith('http://') or avatar.startswith('https://'):
                data['avatar'] = avatar
            else:
                base = getattr(settings, 'CURRENT_URL', '')
                data['avatar'] = f"{base}{avatar}"
        else:
            data['avatar'] = None
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=False)

    class Meta:
        model = User
        fields = ("name", "email", "password")
        extra_kwargs = {
            "email": {"required": False},
            "name": {"required": False},
        }

    def validate_email(self, value):
        if not value:
            return value
        user = self.instance
        qs = User.objects.filter(email=value)
        if user:
            qs = qs.exclude(pk=user.pk)
        if qs.exists():
            raise serializers.ValidationError("E-mail já está em uso.")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if password:
            instance.set_password(password)
        instance.save()
        return instance