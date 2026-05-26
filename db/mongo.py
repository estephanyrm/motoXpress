from pymongo import MongoClient


class ConexionMongoDB:
    _cliente = MongoClient("mongodb://localhost:27017/")
    _db = _cliente["MotoXpress"]

    @classmethod
    def get_collection(cls, collection_name):
        return cls._db[collection_name]