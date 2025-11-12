from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from api.accounts.models import User
from api.client.models import Client
from api.vehicle.models import Vehicle, TypeVehicle
from api.rent.models import Rental
from api.rent.serializer import (
    RentSerializer,
    RentListSerializer,
    RentServiceUpdateSerializer
)


class RentalModelTestCase(TestCase):
    """
    Testes para o modelo Rental.
    """

    def setUp(self):
        """
        Configura dados de teste.
        """
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
            cpf='12345678900'
        )
        self.client = Client.objects.create(user=self.user)
        self.vehicle = Vehicle.objects.create(
            brand='Toyota',
            model='Corolla',
            year=2024,
            quantity=5,
            type_vehicle=TypeVehicle.CAR
        )

    def test_rental_creation(self):
        """
        Testa criação de aluguel.
        """
        rental = Rental.objects.create(
            client=self.client,
            vehicle=self.vehicle,
            start_date=date.today(),
            returned=False
        )
        self.assertIsNotNone(rental.id)
        self.assertEqual(rental.client, self.client)
        self.assertEqual(rental.vehicle, self.vehicle)
        self.assertFalse(rental.returned)

    def test_rental_str_representation(self):
        """
        Testa representação string do aluguel.
        """
        rental = Rental.objects.create(
            client=self.client,
            vehicle=self.vehicle,
            start_date=date.today()
        )
        expected_str = f"Aluguel de {self.vehicle} por {self.user.name}"
        self.assertEqual(str(rental), expected_str)

    def test_rental_ordering(self):
        """
        Testa ordenação de aluguéis por data de início (mais recente primeiro).
        """
        rental1 = Rental.objects.create(
            client=self.client,
            vehicle=self.vehicle,
            start_date=date.today() - timedelta(days=5)
        )
        rental2 = Rental.objects.create(
            client=self.client,
            vehicle=self.vehicle,
            start_date=date.today()
        )
        rentals = list(Rental.objects.all())
        self.assertEqual(rentals[0], rental2)
        self.assertEqual(rentals[1], rental1)


class RentSerializerTestCase(TestCase):
    """
    Testes para os serializers de aluguel.
    """

    def setUp(self):
        """
        Configura dados de teste.
        """
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
            cpf='12345678900'
        )
        self.client = Client.objects.create(user=self.user)
        self.vehicle = Vehicle.objects.create(
            brand='Toyota',
            model='Corolla',
            year=2024,
            quantity=5,
            type_vehicle=TypeVehicle.CAR
        )

    def test_rent_serializer_valid_data(self):
        """
        Testa serializer com dados válidos.
        """
        data = {
            'client': str(self.client.id),
            'vehicle': str(self.vehicle.id),
            'start_date': date.today()
        }
        serializer = RentSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_rent_serializer_invalid_past_date(self):
        """
        Testa validação de data no passado.
        """
        data = {
            'client': str(self.client.id),
            'vehicle': str(self.vehicle.id),
            'start_date': date.today() - timedelta(days=1)
        }
        serializer = RentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('start_date', serializer.errors)

    def test_rent_serializer_unavailable_vehicle(self):
        """
        Testa validação de veículo indisponível.
        """
        self.vehicle.quantity = 0
        self.vehicle.is_available = False
        self.vehicle.save()

        data = {
            'client': str(self.client.id),
            'vehicle': str(self.vehicle.id),
            'start_date': date.today()
        }
        serializer = RentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('vehicle', serializer.errors)

    def test_rent_list_serializer_includes_related_data(self):
        """
        Testa que RentListSerializer inclui dados relacionados.
        """
        rental = Rental.objects.create(
            client=self.client,
            vehicle=self.vehicle,
            start_date=date.today()
        )
        serializer = RentListSerializer(rental)
        data = serializer.data
        self.assertIn('client_data', data)
        self.assertIn('vehicle_data', data)

    def test_rent_service_update_serializer_valid_end_date(self):
        """
        Testa serializer de atualização com data de devolução válida.
        """
        rental = Rental.objects.create(
            client=self.client,
            vehicle=self.vehicle,
            start_date=date.today()
        )
        data = {
            'end_date': date.today() + timedelta(days=7)
        }
        serializer = RentServiceUpdateSerializer(rental, data=data, partial=True)
        self.assertTrue(serializer.is_valid())

    def test_rent_service_update_serializer_invalid_end_date(self):
        """
        Testa validação de data de devolução anterior à data de início.
        """
        rental = Rental.objects.create(
            client=self.client,
            vehicle=self.vehicle,
            start_date=date.today()
        )
        data = {
            'end_date': date.today() - timedelta(days=1)
        }
        serializer = RentServiceUpdateSerializer(rental, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn('end_date', serializer.errors)

    def test_rent_service_update_serializer_already_returned(self):
        """
        Testa validação de aluguel já devolvido.
        """
        rental = Rental.objects.create(
            client=self.client,
            vehicle=self.vehicle,
            start_date=date.today(),
            returned=True
        )
        data = {
            'end_date': date.today() + timedelta(days=7)
        }
        serializer = RentServiceUpdateSerializer(rental, data=data, partial=True)
        self.assertFalse(serializer.is_valid())


class RentViewTestCase(TestCase):
    """
    Testes para as views de aluguel.
    """

    def setUp(self):
        """
        Configura dados de teste.
        """
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
            cpf='12345678900'
        )
        self.client = Client.objects.create(user=self.user)
        self.vehicle = Vehicle.objects.create(
            brand='Toyota',
            model='Corolla',
            year=2024,
            quantity=5,
            type_vehicle=TypeVehicle.CAR
        )

    def test_rent_list_view_uses_select_related(self):
        """
        Testa que RentListView usa select_related para otimização.
        """
        Rental.objects.create(
            client=self.client,
            vehicle=self.vehicle,
            start_date=date.today()
        )
        from api.rent.views import RentListView
        view = RentListView()
        queryset = view.get_queryset()
        self.assertIn('client__user', str(queryset.query))
        self.assertIn('vehicle', str(queryset.query))

    def test_rent_detail_view_uses_select_related(self):
        """
        Testa que RentDetailView usa select_related para otimização.
        """
        rental = Rental.objects.create(
            client=self.client,
            vehicle=self.vehicle,
            start_date=date.today()
        )
        from api.rent.views import RentDetailView
        view = RentDetailView()
        queryset = view.get_queryset()
        self.assertIn('client__user', str(queryset.query))
        self.assertIn('vehicle', str(queryset.query))
