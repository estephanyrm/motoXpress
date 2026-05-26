from typing import Optional

from db.mongo import ConexionMongoDB
from model.VO.FinanciacionVO import FinanciacionVO


def _a_vo(doc) -> Optional[FinanciacionVO]:

    if doc is None:
        return None

    return FinanciacionVO(
        id_financiacion=doc.get("id_financiacion"),
        cuotas=doc.get("cuotas"),
        interes=doc.get("interes"),
        monto_cuota=doc.get("monto_cuota"),
        id_venta=doc.get("id_venta")
    )


class FinanciacionDAO:

    @staticmethod
    def obtener_por_venta(
            id_venta: int) -> Optional[FinanciacionVO]:

        coleccion = ConexionMongoDB.get_collection(
            "Financiacion"
        )

        doc = coleccion.find_one({
            "id_venta": id_venta
        })

        return _a_vo(doc)

    @staticmethod
    def insertar(
            financiacion: FinanciacionVO) -> int:

        coleccion = ConexionMongoDB.get_collection(
            "Financiacion"
        )

        ultimo = coleccion.find_one(
            sort=[("id_financiacion", -1)]
        )

        nuevo_id = 1

        if ultimo:
            nuevo_id = ultimo["id_financiacion"] + 1

        coleccion.insert_one({
            "id_financiacion": nuevo_id,
            "cuotas": financiacion.cuotas,
            "interes": financiacion.interes,
            "monto_cuota": financiacion.monto_cuota,
            "id_venta": financiacion.id_venta
        })

        return nuevo_id

    @staticmethod
    def eliminar(
            id_financiacion: int) -> None:

        coleccion = ConexionMongoDB.get_collection(
            "Financiacion"
        )

        coleccion.delete_one({
            "id_financiacion": id_financiacion
        })