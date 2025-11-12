from django.db import models
from uuid import uuid4
from api.vehicle.models import Vehicle
from api.client.models import Client


class Rental(models.Model):
    """
    Modelo para representar aluguéis de veículos.
    
    Attributes:
        id: Identificador único UUID do aluguel.
        client: Cliente que realizou o aluguel (ForeignKey para Client).
        vehicle: Veículo alugado (ForeignKey para Vehicle).
        start_date: Data de início do aluguel.
        end_date: Data de devolução do veículo (pode ser None se ainda não devolvido).
        returned: Indica se o veículo foi devolvido.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='rentals',
        help_text="Cliente que realizou o aluguel"
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='rentals',
        help_text="Veículo alugado"
    )
    start_date = models.DateField(null=False, help_text="Data de início do aluguel")
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="Data de devolução do veículo"
    )
    returned = models.BooleanField(
        default=False,
        help_text="Indica se o veículo foi devolvido"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Aluguel'
        verbose_name_plural = 'Aluguéis'

    def __str__(self):
        return f"Aluguel de {self.vehicle} por {self.client.user.name}"
