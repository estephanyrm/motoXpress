from typing import Optional, List
from datetime import datetime

from db.mongo import ConexionMongoDB

from model.VO.VentaVO import VentaVO

from model.DAO.ClienteDAO import ClienteDAO
from model.DAO.MotoDAO import MotoDAO
from model.DAO.EmpleadoDAO import EmpleadoDAO
from model.DAO.FinanciacionDAO import FinanciacionDAO


class VentaDAO:

    @staticmethod
    def listar_por_cliente(
            id_cliente: int) -> List[VentaVO]:

        coleccion = ConexionMongoDB.get_collection("Venta")

        ventas = []

        for doc in coleccion.find({"id_cliente": id_cliente}):

            moto = MotoDAO.obtener_por_id(
                doc["id_moto"]
            )

            venta = VentaVO(
                id_venta=doc["id_venta"],
                fecha_venta=doc["fecha_venta"],
                precio_final=doc["precio_final"],
                tipo_pago=doc["tipo_pago"],
                id_cliente=doc["id_cliente"],
                id_moto=doc["id_moto"],
                id_empleado=doc["id_empleado"]
            )

            venta._moto_cache = moto

            id_v = doc["id_venta"]

            venta._financiacion_loader = (
                lambda id_v=id_v:
                FinanciacionDAO.obtener_por_venta(id_v)
            )

            ventas.append(venta)

        return ventas

    @staticmethod
    def listar_por_periodo(
            fecha_inicio: str,
            fecha_fin: str) -> List[VentaVO]:

        coleccion = ConexionMongoDB.get_collection("Venta")

        ventas = []

        consulta = {
            "fecha_venta": {
                "$gte": fecha_inicio,
                "$lte": fecha_fin
            }
        }

        documentos = coleccion.find(
            consulta
        ).sort("fecha_venta", -1)

        for doc in documentos:

            moto = MotoDAO.obtener_por_id(
                doc["id_moto"]
            )

            venta = VentaVO(
                id_venta=doc["id_venta"],
                fecha_venta=doc["fecha_venta"],
                precio_final=doc["precio_final"],
                tipo_pago=doc["tipo_pago"],
                id_cliente=doc["id_cliente"],
                id_moto=doc["id_moto"],
                id_empleado=doc["id_empleado"]
            )

            venta._moto_cache = moto

            id_v = doc["id_venta"]

            venta._financiacion_loader = (
                lambda id_v=id_v:
                FinanciacionDAO.obtener_por_venta(id_v)
            )

            ventas.append(venta)

        return ventas

    @staticmethod
    def obtener_por_id(
            id_venta: int) -> Optional[VentaVO]:

        coleccion = ConexionMongoDB.get_collection(
            "Venta"
        )

        doc = coleccion.find_one({
            "id_venta": id_venta
        })

        if doc is None:
            return None

        venta = VentaVO(
            id_venta=doc["id_venta"],
            fecha_venta=doc["fecha_venta"],
            precio_final=doc["precio_final"],
            tipo_pago=doc["tipo_pago"],
            id_cliente=doc["id_cliente"],
            id_moto=doc["id_moto"],
            id_empleado=doc["id_empleado"]
        )

        venta._cliente_cache = (
            ClienteDAO.obtener_por_id(
                doc["id_cliente"]
            )
        )

        venta._moto_cache = (
            MotoDAO.obtener_por_id(
                doc["id_moto"]
            )
        )

        venta._empleado_cache = (
            EmpleadoDAO.obtener_por_id(
                doc["id_empleado"]
            )
        )

        venta.financiacion = (
            FinanciacionDAO.obtener_por_venta(
                doc["id_venta"]
            )
        )

        return venta

    @staticmethod
    def insertar(
            venta: VentaVO) -> int:

        coleccion = ConexionMongoDB.get_collection(
            "Venta"
        )

        ultimo = coleccion.find_one(
            sort=[("id_venta", -1)]
        )

        nuevo_id = 1

        if ultimo:
            nuevo_id = ultimo["id_venta"] + 1

        coleccion.insert_one({
            "id_venta": nuevo_id,
            "fecha_venta": datetime.now().strftime("%Y-%m-%d"),
            "precio_final": venta.precio_final,
            "tipo_pago": venta.tipo_pago,
            "id_cliente": venta.id_cliente,
            "id_moto": venta.id_moto,
            "id_empleado": venta.id_empleado
        })

        venta.id_venta = nuevo_id

        if venta.financiacion:

            venta.financiacion.id_venta = nuevo_id

            FinanciacionDAO.insertar(
                venta.financiacion
            )

        MotoDAO.actualizar_estado(
            venta.id_moto,
            "vendida"
        )

        return nuevo_id

    @staticmethod
    def eliminar(
            id_venta: int) -> None:

        coleccion = ConexionMongoDB.get_collection(
            "Venta"
        )

        coleccion.delete_one({
            "id_venta": id_venta
        })