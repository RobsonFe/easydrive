import logging
from urllib.parse import quote_plus
from pymongo import MongoClient
from django.conf import settings

logger = logging.getLogger(__name__)


class NullCollection:
    """Objeto nulo que fornece as operações mínimas usadas pela aplicação
    quando não há conexão com o MongoDB. Evita exceptions e retorna valores
    seguros (listas vazias / None)."""
    def __init__(self, name=None):
        self.name = name

    def insert_one(self, *args, **kwargs):
        return None

    def find(self, *args, **kwargs):
        return []

    def find_one(self, *args, **kwargs):
        return None

    def update_one(self, *args, **kwargs):
        return None

    def update_many(self, *args, **kwargs):
        return None

    def delete_one(self, *args, **kwargs):
        return None

    def limit(self, n):
        return []


class NullDBConnection:
    def __init__(self):
        self._collections = {}

    def get_collection(self, name):
        if name not in self._collections:
            self._collections[name] = NullCollection(name)
        return self._collections[name]


class DBConnectionMongoHandler:
    def __init__(self):
        self.__connection_string = None
        self.__database_name = None
        self.__client = None
        self.__db_connection = None

        try:
            username = settings.MONGO_USERNAME
            password = settings.MONGO_PASSWORD
            host = settings.MONGO_HOST
            db_name = settings.MONGO_DB_NAME

            if username and password:
                # Importante: encode para suportar caracteres especiais (ex: '@', '#', ':')
                enc_user = quote_plus(username)
                enc_pass = quote_plus(password)
                self.__connection_string = (
                    f"mongodb+srv://{enc_user}:{enc_pass}@{host}/?retryWrites=true&w=majority&appName=Cluster0"
                )
            else:
                self.__connection_string = f'mongodb://{host}:27017/'

            self.__database_name = db_name

        except Exception as e:
            logger.warning(f"Falha ao ler configuração de mongo do settings.py: {e}")


    def connect_to_db(self):
        if not self.__connection_string or not self.__database_name:
            raise RuntimeError("MongoDB configuration not provided")

        self.__client = MongoClient(self.__connection_string)
        self.__db_connection = self.__client[self.__database_name]

    def get_db_connection(self):
        if self.__db_connection is not None:
            return self.__db_connection

        try:
            self.connect_to_db()
            return self.__db_connection
        except Exception as e:
            logger.warning(f"Não foi possível conectar ao MongoDB: {e}")
            return NullDBConnection()

    def get_db_client(self):
        return self.__client

connection = DBConnectionMongoHandler()
