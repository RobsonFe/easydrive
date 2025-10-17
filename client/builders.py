from client.models import Client
from account.models import User


class ClientBuilder:

    def __init__(self):
        self._user = None
        self._total_rentals = 0

    def set_user(self, user: User) -> "ClientBuilder":
        self._user = user
        return self

    def set_total_rentals(self, total_rentals: int) -> "ClientBuilder":
        self._total_rentals = total_rentals
        return self

    def build(self) -> Client:
        if self._user is None:
            raise ValueError("Deve ser definido um usuário")

        client = Client(user=self._user, total_rentals=self._total_rentals)
        client.save()
        return client
