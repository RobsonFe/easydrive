from api.model.vehicle_model import TypeVehicle, Vehicle

class VehicleBuilder:
    
    def __init__(self):
        self._brand = ""
        self._model = ""
        self._year = 0
        self._quantity = 0
        self._type_vehicle = TypeVehicle.CAR
        self._description = ""
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
    
    def set_quantity(self, quantity: int) -> 'VehicleBuilder':
        self._quantity = quantity  
        return self
    
    def set_type_vehicle(self, type_vehicle: TypeVehicle) -> 'VehicleBuilder':
        self._type_vehicle = type_vehicle
        return self
    
    def set_description(self, description: str) -> 'VehicleBuilder':
        self._description = description
        return self

    def set_is_available(self, is_available: bool) -> 'VehicleBuilder':
        self._is_available = is_available  
        return self
    
    def build(self) -> Vehicle:
        return Vehicle(brand=self._brand, model=self._model, year=self._year, quantity=self._quantity, type_vehicle=self._type_vehicle, description= self._description, is_available=self._is_available)
