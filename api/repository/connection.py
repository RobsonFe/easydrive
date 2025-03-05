from pymongo import MongoClient
from .mongo_db_configs import mongo_db_infos

class DBConnectionMongoHandler:
    def __init__(self):
        self.__connection_string = 'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(
            mongo_db_infos['USERNAME'],
            mongo_db_infos['PASSWORD'],
            mongo_db_infos['HOST'],
            mongo_db_infos['DB_NAME'],
        )
        self.__database_name = mongo_db_infos['DB_NAME']
        self.__client = None
        self.__db_connection =None
        self.connect_to_db()
        
    def connect_to_db(self):
        self.__client = MongoClient(self.__connection_string)
        self.__db_connection = self.__client[self.__database_name]
    
    def get_db_connection(self):
        return self.__db_connection
    
    def get_db_client(self):
        return self.__client