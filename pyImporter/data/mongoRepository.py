from pymongo import MongoClient
from pymongo.database import Database
import datetime


class MongoRepository(object):
    _db: Database

    def __init__(self, connection_string: str, bd: str):
        # exemplo conn string mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase
        self._db = MongoClient(connection_string)[bd]

    def recuperar_collection(self, collection: str):
        return self._db.get_collection(collection)

    def insere(self, collection: str, itens: list = []):
        self.recuperar_collection(collection).insert_many(itens)

    def consultar(self, collection: str, consulta: object):
        return self.recuperar_collection(collection).find(consulta)

    def criar_indice(self, collection: str, indice: str):
        return self.recuperar_collection(collection).create_index(indice)

    def recupera_tempo(self, collection: str, consulta: object):
        init_time = datetime.datetime.now()
        self.consultar(collection, consulta)
        end_time = datetime.datetime.now()

        return end_time - init_time
