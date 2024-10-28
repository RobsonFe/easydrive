from api.model.user_model import User


class UserBuilder:
    
    def __init__(self):
        self._username = ""
        self._name=""
        self._email= ""
        self._password= ""
        
    
    def set_username(self, username: str) ->'UserBuilder':
        self._username
        return self
    
    def set_name(self,  name: str) -> 'UserBuilder':
        self._name
        return self
    
    def set_email(self, email: str) -> 'UserBuilder':
        self._email
        return self
    
    def set_password(self, password:str) -> 'UserBuilder':
        self._password
        return self

    def build(self) -> User:
        
        if not self.set_email:
            raise ValueError('Usuários devem ter um endereço de email.')
        if not self.set_username:
            raise ValueError('Usuários devem ter um nome de usuário.')
        if not self.set_password:
            raise ValueError('Usuários devem ter uma senha.')
        
        return User.objects.create_user(self._username, self._name, self._email, self.set_password)
