from adapters.api.config.mongo import connection
from pymongo.errors import PyMongoError
from django.utils import timezone

class MongoAdapter:
    """
    Classe para manipular documentos MongoDB de forma síncrona e assíncrona.
    Recebe um nome de coleção (collection) no construtor e fornece métodos
    para operações CRUD (Create, Read, Update, Delete) nessa coleção.
    """

    def __init__(self, collection_name: str):
        try:
            # Acessa a conexão com o banco de dados e a collection.
            db_handler = connection.DBConnectionMongoHandler().get_db_connection()
            self.collection = db_handler.get_collection(collection_name)
        except PyMongoError as e:
            raise ConnectionError(f"Erro ao conectar ao MongoDB: {e}")

    def save_error(self, user, endpoint, method, error, payload):
        """
        Salva um log de erro no banco de dados.
        """
        try:
            log = {
                "timestamp": timezone.now().isoformat(),
                "user": user,
                "endpoint": endpoint,
                "method": method,
                "error": error,
                "payload": payload,
            }
            self.collection.insert_one(log)
            return True
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao salvar log de erro: {e}")

    # ----------------------------------------
    # Métodos de Leitura (Read)
    # ----------------------------------------

    def find_one(self, query: dict, projection: dict = None) -> dict:
        """Busca um único documento na collection."""
        try:
            return self.collection.find_one(query, projection)
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao buscar documento: {e}")

    def find_many(self, query: dict, limit: int = None) -> list:
        """Busca múltiplos documentos na collection."""
        try:
            cursor = self.collection.find(query)
            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao buscar documentos: {e}")

    def count_documents(self, query: dict) -> int:
        """Conta o número de documentos que correspondem a uma query."""
        try:
            return self.collection.count_documents(query)
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao contar documentos: {e}")

    def aggregate(self, pipeline: list) -> list:
        """Executa um pipeline de agregação."""
        try:
            return list(self.collection.aggregate(pipeline))
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao executar agregação: {e}")

    # ----------------------------------------
    # Métodos de Escrita (Create & Update)
    # ----------------------------------------

    def insert_one(self, document: dict) -> bool:
        """Insere um único documento na collection."""
        try:
            result = self.collection.insert_one(document)
            return result
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao salvar documento: {e}")

    def insert_many(self, documents: list) -> bool:
        """Insere múltiplos documentos na collection."""
        try:
            result = self.collection.insert_many(documents)
            return result
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao salvar documentos: {e}")

    def update_one(self, query: dict, update: dict, array_filters: list = None, upsert: bool = False):
        """Atualiza um único documento na collection.
        :param upsert: se True, cria o documento caso não exista.
        Retorna o resultado bruto do PyMongo (UpdateResult).
        """
        try:
            result = self.collection.update_one(
                query,
                update,
                array_filters=array_filters,
                upsert=upsert,
            )
            return result
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao atualizar documento: {e}")

    def update_many(self, query: dict, update: dict, array_filters: list = None, upsert: bool = False):
        """Atualiza múltiplos documentos na collection.
        :param upsert: PyMongo permite upsert em update_many também.
        Retorna UpdateResult.
        """
        try:
            result = self.collection.update_many(
                query,
                update,
                array_filters=array_filters,
                upsert=upsert,
            )
            return result
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao atualizar documentos: {e}")

    # ----------------------------------------
    # Métodos de Deleção (Delete)
    # ----------------------------------------

    def delete_one(self, query: dict) -> bool:
        """Deleta um único documento da collection."""
        try:
            result = self.collection.delete_one(query)
            return result
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao deletar documento: {e}")

    def delete_many(self, query: dict) -> bool:
        """Deleta múltiplos documentos da collection."""
        try:
            result = self.collection.delete_many(query)
            return result
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao deletar documentos: {e}")