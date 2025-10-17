from adapters.api.config.mongo.async_connection import async_connection
from pymongo.errors import PyMongoError

class AsyncMongoAdapter:
    """
    Classe para manipular documentos MongoDB de forma NATIVA e assíncrona com Motor.
    """
    def __init__(self, collection_name: str):
        db_handler = async_connection.get_db_connection()
        self.collection = db_handler[collection_name] 
        
    # ----------------------------------------
    # Métodos de Leitura (Read)
    # ----------------------------------------

    async def find_one(self, query: dict, projection: dict = None) -> dict:
        """Busca um único documento na collection."""
        try:
            return await self.collection.find_one(query, projection)
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao buscar documento: {e}")

    async def find_many(self, query: dict, limit: int = None) -> list:
        """
        Busca múltiplos documentos. 
        Se o limite for None, retorna todos os documentos encontrados.
        Se limit for None, to_list(length=None) busca todos os itens.
        Se limit for um número, to_list(length=number) busca aquela quantidade.
        """
        try:
            cursor = self.collection.find(query)
            return await cursor.to_list(length=limit)
        
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao buscar documentos: {e}")

    async def count_documents(self, query: dict) -> int:
        """Conta o número de documentos que correspondem a uma query."""
        try:
            return await self.collection.count_documents(query)
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao contar documentos: {e}")

    async def aggregate(self, pipeline: list) -> list:
        """Executa um pipeline de agregação."""
        try:
            cursor = self.collection.aggregate(pipeline)
            return await cursor.to_list(length=None) # length=None para pegar todos os resultados
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao executar agregação: {e}")

    # ----------------------------------------
    # Métodos de Escrita (Create & Update)
    # ----------------------------------------

    async def insert_one(self, document: dict):
        """Insere um único documento na collection."""
        try:
            return await self.collection.insert_one(document)
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao salvar documento: {e}")

    async def insert_many(self, documents: list):
        """Insere múltiplos documentos na collection."""
        try:
            return await self.collection.insert_many(documents)
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao salvar documentos: {e}")

    async def update_one(self, query: dict, update: dict, array_filters: list = None, upsert: bool = False):
        """Atualiza um único documento na collection.
        :param upsert: se True, cria o documento se não existir.
        """
        try:
            return await self.collection.update_one(query, update, array_filters=array_filters, upsert=upsert)
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao atualizar documento: {e}")

    async def update_many(self, query: dict, update: dict, array_filters: list = None, upsert: bool = False):
        """Atualiza múltiplos documentos na collection.
        Obs: update_many do Motor não suporta upsert explícito (apenas update_one). Ignora se passado.
        """
        try:
            return await self.collection.update_many(query, update, array_filters=array_filters)
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao atualizar documentos: {e}")

    # ----------------------------------------
    # Métodos de Deleção (Delete)
    # ----------------------------------------

    async def delete_one(self, query: dict):
        """Deleta um único documento da collection."""
        try:
            return await self.collection.delete_one(query)
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao deletar documento: {e}")

    async def delete_many(self, query: dict):
        """Deleta múltiplos documentos da collection."""
        try:
            return await self.collection.delete_many(query)
        except PyMongoError as e:
            raise RuntimeError(f"Erro ao deletar documentos: {e}")