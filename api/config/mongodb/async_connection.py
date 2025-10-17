import logging
from urllib.parse import quote_plus
import motor.motor_asyncio
from django.conf import settings

logger = logging.getLogger(__name__)


class AsyncNullCollection:
    """Versão assíncrona do NullCollection. Os métodos são coroutines."""
    def __init__(self, name=None):
        self.name = name

    async def insert_one(self, *args, **kwargs):
        return None

    async def find(self, *args, **kwargs):
        return []

    async def find_one(self, *args, **kwargs):
        return None

    async def update_one(self, *args, **kwargs):
        return None

    async def update_many(self, *args, **kwargs):
        return None

    async def delete_one(self, *args, **kwargs):
        return None

    def limit(self, n):
        return self


class AsyncNullDBConnection:
    """Versão assíncrona do NullDBConnection."""
    def __init__(self):
        self._collections = {}

    def __getitem__(self, name):
        # Permite o acesso como `db['collection_name']`
        if name not in self._collections:
            self._collections[name] = AsyncNullCollection(name)
        return self._collections[name]

class AsyncDBConnectionMongoHandler:
    def __init__(self):
        self.db = None
        try:
            username = settings.MONGO_USERNAME
            password = settings.MONGO_PASSWORD
            host = settings.MONGO_HOST
            db_name = settings.MONGO_DB_NAME

            if username and password:
                # Encode credenciais para suportar caracteres especiais
                enc_user = quote_plus(username)
                enc_pass = quote_plus(password)
                connection_string = (
                    f"mongodb+srv://{enc_user}:{enc_pass}@{host}/?retryWrites=true&w=majority&appName=Cluster0"
                )
            else:
                connection_string = f'mongodb://{host}:27017/'
            
            self.client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
            self.db = self.client[db_name]

        except Exception as e:
            logger.error(f"Não foi possível conectar ao MongoDB (async): {e}")
            self.db = AsyncNullDBConnection()

    def get_db_connection(self):
        return self.db

async_connection = AsyncDBConnectionMongoHandler()