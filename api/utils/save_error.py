from api.config.mongodb.connection import DBConnectionMongoHandler
from pymongo.errors import PyMongoError
from django.utils import timezone


class ErrorLogger:
    """Utilitário para persistir logs de erro em uma coleção MongoDB.

    Attributes:
        collection: Instância da coleção MongoDB onde os erros serão salvos.
    """

    def __init__(self, collection_name: str):
        """Inicializa o logger resolvendo a coleção.

        Args:
            collection_name: Nome da coleção MongoDB destinada aos logs.

        Raises:
            ConnectionError: Quando ocorre falha ao obter a conexão ou a coleção.
        """
        try:
            db_handler = DBConnectionMongoHandler().get_db_connection()
            self.collection = db_handler.get_collection(collection_name)
        except PyMongoError as e:
            raise ConnectionError(f"Erro ao conectar ao MongoDB: {e}")

    def save_error(self, user: str, endpoint: str, method: str, error: str, payload):
        """Persiste um registro de erro na coleção MongoDB.

        Args:
            user: Identificação do usuário (e-mail ou literal indicando não autenticado).
            endpoint: Caminho do endpoint que originou o erro.
            method: Método HTTP da requisição.
            error: Representação textual ou JSON do erro ocorrido.
            payload: Corpo sanitizado da requisição (ou None).

        Returns:
            bool: True em caso de sucesso.

        Raises:
            RuntimeError: Caso ocorra falha ao inserir o documento na coleção.
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