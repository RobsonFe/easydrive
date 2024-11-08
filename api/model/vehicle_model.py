from django.db import models
from uuid import uuid4

class TypeVehicle(models.TextChoices):
    CAR = 'Carro'
    MOTORCYCLE = 'Moto'

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=0)
    type_vehicle = models.CharField(max_length=10, choices=TypeVehicle.choices, default=TypeVehicle.CAR)    
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) ({self.quantity}) ({self.type_vehicle})"