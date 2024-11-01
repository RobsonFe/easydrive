from api.model.vehicle_model import Vehicle

class VehicleBuilder:
    
    def __init__(self):
        self._brand = ""
        self._model = ""
        self._year = 0
        self._is_available = True 

    def set_brand(self, brand: str) -> 'VehicleBuilder':
        self._brand = brand 
        return self

    def set_model(self, model: str) -> 'VehicleBuilder':
        self._model = model 
        return self

    def set_year(self, year: int) -> 'VehicleBuilder':
        self._year = year 
        return self

    def set_is_available(self, is_available: bool) -> 'VehicleBuilder':
        self._is_available = is_available  
        return self
    
    def build(self) -> Vehicle:
        return Vehicle(brand=self._brand, model=self._model, year=self._year, is_available=self._is_available)
