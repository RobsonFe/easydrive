from api.model.client_model import Client
from api.model.rent_model import Rental
from api.model.vehicle_model import Vehicle
from datetime import date


class RentBuilder:
    def __init__(self):
        self._client = None
        self._vehicle = None
        self._start_date = None
        self._end_date = None
        self._returned = False

    def set_client(self, client: Client) -> 'RentBuilder':
        self._client = client
        return self

    def set_vehicle(self, vehicle: Vehicle) -> 'RentBuilder':
        self._vehicle = vehicle
        return self

    def set_start_date(self, start_date: date) -> 'RentBuilder':
        self._start_date = start_date
        return self

    def set_end_date(self, end_date: date) -> 'RentBuilder':
        self._end_date = end_date
        return self

    def set_returned(self, returned: bool) -> 'RentBuilder':
        self._returned = returned
        return self

    def build(self) -> Rental:
        return Rental(
            client=self._client,
            vehicle=self._vehicle,
            start_date=self._start_date,
            end_date=self._end_date,
            returned=self._returned,
        )
