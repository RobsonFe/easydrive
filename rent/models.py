from django.db import models
from uuid import uuid4
from client.models import Client
from vehicle.models import Vehicle


class Rental(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(blank=True, null=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"Aluguel de {self.vehicle} por {self.client.user.name}"
