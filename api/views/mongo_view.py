from django.http import JsonResponse
import datetime
from api.repository import connection


class MongoLogger:
    def __init__(self):
        self.db_handler = connection.DBConnectionMongoHandler().get_db_connection()
        self.db = self.db_handler.get_collection("logs")

    def salvar_log(self, usuario, endpoint, metodo, erro):
        log = {
            "data_hora": str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')),
            "usuario": usuario,
            "endpoint": endpoint,
            "metodo": metodo,
            "erro": erro
        }
        self.db.insert_one(log)  # Insere no MongoDB o dicionario do log


def listar_logs(request):
    db_handler = connection.DBConnectionMongoHandler().get_db_connection()
    db = db_handler.get_collection("logs")

    # Retorna todos os logs ordenados pela data_hora
    logs = list(db.find().sort("data_hora", -1))

    for log in logs:
        log["_id"] = str(log["_id"])

    return JsonResponse({"logs": logs}, safe=False)
