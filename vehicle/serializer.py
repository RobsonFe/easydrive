from rest_framework import serializers
from vehicle.models import TypeVehicle, Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    type_vehicle = serializers.ChoiceField(
        choices=TypeVehicle.choices, default=TypeVehicle.CAR)

    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'year', 'quantity',
                  'type_vehicle', 'description', 'is_available']
        extra_kwargs = {'is_available': {'read_only': True}}