from api.model.vehicle_model import Vehicle


class VehicleBuilder:
    
    def __init__(self):
        self._brand = ""
        self.model = ""
        self._year = 0
        self._is_available = bool
        
    
    def set_brand(self, brand: str) -> 'VehicleBuilder':
        self._brand
        return self
    
    def set_model(self,  model: str) -> 'VehicleBuilder':
        self.model
        return self
    
    def set_year(self,  year: int) -> 'VehicleBuilder':
        self._year
        return self
    
    def set_is_available(self, is_available: bool) -> 'VehicleBuilder':
        self._is_available
        return self
    
    def build(self) -> Vehicle:
        return Vehicle(self._brand, self.model, self._year, self._is_available)

