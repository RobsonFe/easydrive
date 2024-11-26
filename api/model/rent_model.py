from django.db import models
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.utils import timezone
from api.model.vehicle_model import Vehicle


class Rental(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client = models.ForeignKey('api.Client', on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(blank=True, null=True)
    returned = models.BooleanField(default=False)

    # # Validação das datas, um dos requisitos do cliente.
    # def clean(self):
    #     # O end_date não pode ser menor que a start_date
    #     if self.end_date < self.start_date:
    #         raise ValidationError(
    #             'A data de término do aluguel não pode ser anterior à data de início.')

    #     # O start_date não pode estar no passado
    #     if self.start_date < timezone.now().date():  # Converte para date
    #         raise ValidationError(
    #             'A data de início do aluguel não pode ser no passado.')

    # def save(self, *args, **kwargs):
    #     # Validar o objeto antes de salvar
    #     # self.full_clean()
    #     super(Rental, self).save(*args, **kwargs)
    #     self.vehicle.is_available = not self.returned
    #     self.vehicle.save()

    def __str__(self):
        return f"Aluguel de {self.vehicle} por {self.client.user.name}"
