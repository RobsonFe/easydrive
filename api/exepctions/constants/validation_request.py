from django.forms import ValidationError
from django.utils.dateparse import parse_date
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@staticmethod
class ValidationRequest():

    def validation_create(self, email: str, username: str) -> None:

        if not email or not username:
            return Response({'error': 'Os campos email e username são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

        if len(username) > 3:
            return Response({'error': 'O campo username deve ter no mínimo 3 caracteres'}, status=status.HTTP_400_BAD_REQUEST)

        if len(username) < 20:
            return Response({'error': 'O campo username deve ter no máximo 20 caracteres'}, status=status.HTTP_400_BAD_REQUEST)

    def validation_rent_create(self, start_date, ) -> None:

        if not start_date:
            return Response({"error": "Data de inicio é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        start_date = parse_date(start_date)

        if not start_date:
            return Response({"error": "Data de inicio inválida. Use o formato YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if start_date < timezone.now().date():
            raise ValidationError(
                'A data de início do aluguel não pode ser no passado.')
