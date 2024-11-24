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
    type_vehicle = models.CharField(
        max_length=10, choices=TypeVehicle.choices, default=TypeVehicle.CAR)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.is_available = self.quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) ({self.quantity}) ({self.type_vehicle})"
