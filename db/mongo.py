from pymongo import MongoClient

class ConexionMongoDB:
    # Cambiar esto a una instancia local si no se quiere correr con el replicaSet
    _cliente = MongoClient('mongodb://localhost:27117,localhost:27118,localhost:27119/?replicaSet=replicaSet')
    _db = _cliente["MotoXpress"]

    @classmethod
    def get_collection(cls, collection_name):
        return cls._db[collection_name]