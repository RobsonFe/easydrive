from account.models import User


class UserBuilder:

    def __init__(self):
        self._username = ""
        self._name = ""
        self._email = ""
        self._password = ""
        self._cpf = ""
        self._address = ""
        self._phone = ""

    def set_username(self, username: str) -> "UserBuilder":
        self._username = username
        return self

    def set_name(self, name: str) -> "UserBuilder":
        self._name = name
        return self

    def set_email(self, email: str) -> "UserBuilder":
        self._email = email
        return self

    def set_password(self, password: str) -> "UserBuilder":
        self._password = password
        return self

    def set_cpf(self, cpf: str) -> "UserBuilder":
        self._cpf = cpf
        return self

    def set_address(self, address: str) -> "UserBuilder":
        self._address = address
        return self

    def set_phone(self, phone: str) -> "UserBuilder":
        self._phone = phone
        return self

    def build(self) -> User:
        if not self._email:
            raise ValueError("Usuários devem ter um endereço de email.")
        if not self._username:
            raise ValueError("Usuários devem ter um nome de usuário.")
        if not self._password:
            raise ValueError("Usuários devem ter uma senha.")
        if not self._cpf:
            raise ValueError("Usuários devem ter um CPF.")

        return User.objects.create_user(
            email=self._email,
            username=self._username,
            name=self._name,
            password=self._password,
            cpf=self._cpf,
            address=self._address,
            phone=self._phone,
        )
