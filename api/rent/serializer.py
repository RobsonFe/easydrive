from rest_framework import serializers
from django.utils import timezone
from api.rent.models import Rental
from api.client.serializer import ClientDetailsSerializer
from api.vehicle.serializer import VehicleSerializer


class RentSerializer(serializers.ModelSerializer):
    """
    Serializer para criação e leitura de aluguéis.
    
    Valida que a data de início não seja no passado e que o veículo
    esteja disponível.
    """
    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = ('id', 'returned', 'created_at', 'updated_at')

    def validate_start_date(self, value):
        """
        Valida que a data de início não seja no passado.
        
        Args:
            value: Data de início do aluguel.
            
        Returns:
            Data validada.
            
        Raises:
            ValidationError: Se a data for no passado.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError(
                'A data de início não pode ser no passado.'
            )
        return value

    def validate(self, attrs):
        """
        Valida que o veículo esteja disponível antes de criar o aluguel.
        
        Args:
            attrs: Dicionário com os atributos validados.
            
        Returns:
            Dicionário de atributos validados.
            
        Raises:
            ValidationError: Se o veículo não estiver disponível.
        """
        vehicle = attrs.get('vehicle')
        if vehicle and not vehicle.is_available:
            raise serializers.ValidationError({
                'vehicle': 'Este veículo não está disponível para aluguel.'
            })
        if vehicle and vehicle.quantity <= 0:
            raise serializers.ValidationError({
                'vehicle': 'Não há unidades disponíveis deste veículo.'
            })
        return attrs


class RentListSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem de aluguéis com dados aninhados.
    
    Inclui informações completas do cliente e veículo usando
    relacionamentos ForeignKey.
    """
    client_data = ClientDetailsSerializer(source='client', read_only=True)
    vehicle_data = VehicleSerializer(source='vehicle', read_only=True)

    class Meta:
        model = Rental
        fields = [
            'id',
            'start_date',
            'end_date',
            'returned',
            'client_data',
            'vehicle_data',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields


class RentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para detalhes completos de um aluguel.
    
    Similar ao RentListSerializer, mas pode incluir campos adicionais
    para visualização detalhada.
    """
    client_data = ClientDetailsSerializer(source='client', read_only=True)
    vehicle_data = VehicleSerializer(source='vehicle', read_only=True)

    class Meta:
        model = Rental
        fields = [
            'id',
            'start_date',
            'end_date',
            'returned',
            'client',
            'vehicle',
            'client_data',
            'vehicle_data',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id', 'client', 'vehicle', 'created_at', 'updated_at')


class RentServiceUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de aluguel (devolução).
    
    Permite apenas atualizar end_date e returned.
    Os campos client e vehicle são read-only.
    """
    class Meta:
        model = Rental
        fields = ['id', 'end_date', 'returned', 'client', 'vehicle']
        read_only_fields = ('id', 'client', 'vehicle')
        extra_kwargs = {
            'end_date': {'required': True},
        }

    def validate_end_date(self, value):
        """
        Valida que a data de devolução não seja anterior à data de início.
        
        Args:
            value: Data de devolução.
            
        Returns:
            Data validada.
            
        Raises:
            ValidationError: Se a data de devolução for anterior à data de início.
        """
        if self.instance and value < self.instance.start_date:
            raise serializers.ValidationError(
                'A data de devolução não pode ser anterior à data de início.'
            )
        return value

    def validate(self, attrs):
        """
        Valida que o aluguel não esteja já devolvido.
        
        Args:
            attrs: Dicionário com os atributos validados.
            
        Returns:
            Dicionário de atributos validados.
            
        Raises:
            ValidationError: Se o aluguel já foi devolvido.
        """
        if self.instance and self.instance.returned:
            raise serializers.ValidationError(
                'Este aluguel já foi devolvido e não pode ser atualizado.'
            )
        return attrs
