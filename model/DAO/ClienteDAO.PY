from typing import Optional, List
from datetime import datetime

from db.mongo import ConexionMongoDB
from model.VO.ClienteVO import ClienteVO


def _a_vo(doc) -> Optional[ClienteVO]:
    if doc is None:
        return None

    return ClienteVO(
        id_cliente=doc.get("id_cliente"),
        nombre=doc.get("nombre"),
        apellido=doc.get("apellido"),
        cedula=doc.get("cedula"),
        telefono=doc.get("telefono"),
        email=doc.get("email"),
        fecha_registro=doc.get("fecha_registro")
    )


class ClienteDAO:

    @staticmethod
    def obtener_por_id(id_cliente: int) -> Optional[ClienteVO]:

        coleccion = ConexionMongoDB.get_collection("Cliente")

        doc = coleccion.find_one({
            "id_cliente": id_cliente
        })

        return _a_vo(doc)

    @staticmethod
    def listar() -> List[ClienteVO]:

        coleccion = ConexionMongoDB.get_collection("Cliente")

        documentos = coleccion.find()

        return [_a_vo(doc) for doc in documentos]

    @staticmethod
    def buscar_por_cedula(
            cedula: str) -> Optional[ClienteVO]:

        coleccion = ConexionMongoDB.get_collection("Cliente")

        doc = coleccion.find_one({
            "cedula": cedula
        })

        return _a_vo(doc)

    @staticmethod
    def insertar(cliente: ClienteVO) -> int:

        coleccion = ConexionMongoDB.get_collection("Cliente")

        ultimo = coleccion.find_one(
            sort=[("id_cliente", -1)]
        )

        nuevo_id = 1

        if ultimo:
            nuevo_id = ultimo["id_cliente"] + 1

        coleccion.insert_one({
            "id_cliente": nuevo_id,
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "cedula": cliente.cedula,
            "telefono": cliente.telefono,
            "email": cliente.email,
            "fecha_registro": datetime.now()
        })

        return nuevo_id