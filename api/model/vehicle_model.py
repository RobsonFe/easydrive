from django.db import models
from uuid import uuid4


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"