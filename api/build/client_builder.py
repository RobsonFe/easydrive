from api.model.client_model import Client
from api.model.user_model import User


class ClientBuilder:
    
    def __init__(self):
        self._user = None
        self._total_rentals = 0
        
    def set_user(self, user:User) -> 'ClientBuilder':
        self._user = user
        return self
    
    def set_total_rental(self, total_rentals: int) -> 'ClientBuilder':
        self._total_rentals = total_rentals
        return self
    
    def build(self) -> Client:
        if not self.set_user:
            raise ValueError("Deve ser definido um usuário")
        
        return Client(self._user, self._total_rentals)
        