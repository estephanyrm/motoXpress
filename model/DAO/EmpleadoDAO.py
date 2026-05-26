from typing import Optional, List

from db.mongo import ConexionMongoDB
from model.VO.EmpleadoVO import EmpleadoVO


def _a_vo(doc) -> Optional[EmpleadoVO]:

    if doc is None:
        return None

    return EmpleadoVO(
        id_empleado=doc.get("id_empleado"),
        nombre=doc.get("nombre"),
        apellido=doc.get("apellido"),
        rol=doc.get("rol"),
        email=doc.get("email")
    )


class EmpleadoDAO:

    @staticmethod
    def obtener_por_id(
            id_empleado: int) -> Optional[EmpleadoVO]:

        coleccion = ConexionMongoDB.get_collection("Empleado")

        doc = coleccion.find_one({
            "id_empleado": id_empleado
        })

        return _a_vo(doc)

    @staticmethod
    def listar() -> List[EmpleadoVO]:

        coleccion = ConexionMongoDB.get_collection("Empleado")

        return [
            _a_vo(doc)
            for doc in coleccion.find()
        ]

    @staticmethod
    def listar_por_rol(
            rol: str) -> List[EmpleadoVO]:

        coleccion = ConexionMongoDB.get_collection("Empleado")

        return [
            _a_vo(doc)
            for doc in coleccion.find({
                "rol": rol
            })
        ]
    
    @staticmethod
    def insertar(empleado: EmpleadoVO) -> int:

        collection = ConexionMongoDB.get_collection("Empleado")

        ultimo = collection.find_one(
            sort=[("id_empleado", -1)]
        )

        nuevo_id = 1

        if ultimo:
            nuevo_id = ultimo["id_empleado"] + 1

        collection.insert_one({
            "id_empleado": nuevo_id,
            "nombre": empleado.nombre,
            "apellido": empleado.apellido,
            "rol": empleado.rol,
            "email": empleado.email
        })

        return nuevo_id