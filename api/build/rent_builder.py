from api.model.client_model import Client
from api.model.vehicle_model import Vehicle


class RentBuilder: 
    
    def __init__(self):
        self._client = None
        self._vehicle = None
        self._start_date = ""
        self._end_date = ""
        self._returned = bool
        
    def set_client(self, client:Client) -> 'RentBuilder':
        self._client =client
        return self
    
    def set_vehicle(self, vehicle:Vehicle) -> 'RentBuilder':
        self._vehicle = vehicle
        return self
    