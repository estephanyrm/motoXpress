from typing import Optional, List

from db.mongo import ConexionMongoDB
from model.VO.CategoriaVO import CategoriaVO


def _a_vo(doc) -> Optional[CategoriaVO]:

    if doc is None:
        return None

    return CategoriaVO(
        id_categoria=doc.get("id_categoria"),
        nombre=doc.get("nombre"),
        descripcion=doc.get("descripcion")
    )


class CategoriaDAO:

    @staticmethod
    def listar_todas() -> List[CategoriaVO]:

        coleccion = ConexionMongoDB.get_collection("Categoria")

        return [
            _a_vo(doc)
            for doc in coleccion.find()
        ]

    @staticmethod
    def obtener_por_id(
            id_categoria: int) -> Optional[CategoriaVO]:

        coleccion = ConexionMongoDB.get_collection("Categoria")

        doc = coleccion.find_one({
            "id_categoria": id_categoria
        })

        return _a_vo(doc)

    @staticmethod
    def insertar(
            nombre: str,
            descripcion: str = None) -> int:

        coleccion = ConexionMongoDB.get_collection("Categoria")

        ultimo = coleccion.find_one(
            sort=[("id_categoria", -1)]
        )

        nuevo_id = 1

        if ultimo:
            nuevo_id = ultimo["id_categoria"] + 1

        coleccion.insert_one({
            "id_categoria": nuevo_id,
            "nombre": nombre,
            "descripcion": descripcion
        })

        return nuevo_id

    @staticmethod
    def actualizar(
            id_categoria: int,
            nombre: str,
            descripcion: str = None) -> None:

        coleccion = ConexionMongoDB.get_collection("Categoria")

        coleccion.update_one(
            {"id_categoria": id_categoria},
            {
                "$set": {
                    "nombre": nombre,
                    "descripcion": descripcion
                }
            }
        )

    @staticmethod
    def eliminar(id_categoria: int) -> None:

        coleccion = ConexionMongoDB.get_collection("Categoria")

        coleccion.delete_one({
            "id_categoria": id_categoria
        })