from typing import Optional, List

from mongo.db.mongo import ConexionMongoDB
from mongo.model.VO.MotoVO import MotoVO
from mongo.model.VO.CategoriaVO import CategoriaVO


def _a_vo(doc) -> MotoVO:
    categorias = [
        CategoriaVO(
            id_categoria=c["id_categoria"],
            nombre=c["nombre"],
            descripcion=c.get("descripcion")
        )
        for c in doc.get("categorias", [])
    ]
    return MotoVO(
        id_moto=doc["id_moto"],
        vin=doc["vin"],
        marca=doc["marca"],
        modelo=doc["modelo"],
        anio=doc["anio"],
        precio=doc["precio"],
        color=doc["color"],
        estado=doc["estado"],
        categorias=categorias
    )


class MotoDAO:

    @staticmethod
    def listar_disponibles() -> List[MotoVO]:
        coleccion = ConexionMongoDB.get_collection("Moto")
        return [_a_vo(doc) for doc in coleccion.find({"estado": "disponible"})]

    @staticmethod
    def obtener_por_id(id_moto: int) -> Optional[MotoVO]:
        coleccion = ConexionMongoDB.get_collection("Moto")
        doc = coleccion.find_one({"id_moto": id_moto})
        return _a_vo(doc) if doc else None

    @staticmethod
    def buscar_por_vin(vin: str) -> Optional[MotoVO]:
        coleccion = ConexionMongoDB.get_collection("Moto")
        doc = coleccion.find_one({"vin": vin})
        return _a_vo(doc) if doc else None

    @staticmethod
    def insertar(moto: MotoVO) -> int:
        coleccion = ConexionMongoDB.get_collection("Moto")
        ultimo = coleccion.find_one(sort=[("id_moto", -1)])
        nuevo_id = (ultimo["id_moto"] + 1) if ultimo else 1
        categorias = [
            {"id_categoria": c.id_categoria, "nombre": c.nombre, "descripcion": c.descripcion}
            for c in moto.categorias
        ]
        coleccion.insert_one({
            "id_moto": nuevo_id, "vin": moto.vin, "marca": moto.marca,
            "modelo": moto.modelo, "anio": moto.anio, "precio": moto.precio,
            "color": moto.color, "estado": moto.estado, "categorias": categorias
        })
        return nuevo_id

    @staticmethod
    def actualizar_estado(id_moto: int, nuevo_estado: str) -> None:
        coleccion = ConexionMongoDB.get_collection("Moto")
        coleccion.update_one({"id_moto": id_moto}, {"$set": {"estado": nuevo_estado}})
