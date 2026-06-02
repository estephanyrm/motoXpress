# model/DAO/VentaDAO.py
from typing import Optional, List

from db.postgres import ConexionPostgres

from model.VO.VentaVO import VentaVO

from model.DAO.ClienteDAO import ClienteDAO
from model.DAO.MotoDAO import MotoDAO          # sigue en Mongo, no cambia
from model.DAO.EmpleadoDAO import EmpleadoDAO
from model.DAO.FinanciacionDAO import FinanciacionDAO


def _a_vo(row) -> VentaVO:
    return VentaVO(
        id_venta=row["id_venta"],
        fecha_venta=row["fecha_venta"],
        precio_final=row["precio_final"],
        tipo_pago=row["tipo_pago"],
        id_cliente=row["id_cliente"],
        id_moto=row["id_moto"],
        id_empleado=row["id_empleado"]
    )


class VentaDAO:

    @staticmethod
    def listar_por_cliente(conn: ConexionPostgres, id_cliente: int) -> List[VentaVO]:
        rows = conn.execute(
            "SELECT * FROM Venta WHERE id_cliente = %s ORDER BY fecha_venta DESC",
            (id_cliente,)
        ).fetchall()

        ventas = []
        for row in rows:
            venta = _a_vo(row)
            venta._moto_cache = MotoDAO.obtener_por_id(row["id_moto"])
            id_v = row["id_venta"]
            venta._financiacion_loader = (
                lambda id_v=id_v: FinanciacionDAO.obtener_por_venta(conn, id_v)
            )
            ventas.append(venta)

        return ventas

    @staticmethod
    def listar_por_periodo(
            conn: ConexionPostgres,
            fecha_inicio: str,
            fecha_fin: str) -> List[VentaVO]:
        rows = conn.execute(
            """
            SELECT * FROM Venta
            WHERE fecha_venta >= %s AND fecha_venta <= %s
            ORDER BY fecha_venta DESC
            """,
            (fecha_inicio, fecha_fin)
        ).fetchall()

        ventas = []
        for row in rows:
            venta = _a_vo(row)
            venta._moto_cache = MotoDAO.obtener_por_id(row["id_moto"])
            id_v = row["id_venta"]
            venta._financiacion_loader = (
                lambda id_v=id_v: FinanciacionDAO.obtener_por_venta(conn, id_v)
            )
            ventas.append(venta)

        return ventas

    @staticmethod
    def obtener_por_id(conn: ConexionPostgres, id_venta: int) -> Optional[VentaVO]:
        row = conn.execute(
            "SELECT * FROM Venta WHERE id_venta = %s",
            (id_venta,)
        ).fetchone()

        if row is None:
            return None

        venta = _a_vo(row)
        venta._cliente_cache  = ClienteDAO.obtener_por_id(conn, row["id_cliente"])
        venta._moto_cache     = MotoDAO.obtener_por_id(row["id_moto"])
        venta._empleado_cache = EmpleadoDAO.obtener_por_id(conn, row["id_empleado"])
        venta.financiacion    = FinanciacionDAO.obtener_por_venta(conn, row["id_venta"])

        return venta

    @staticmethod
    def insertar(conn: ConexionPostgres, venta: VentaVO) -> int:
        row = conn.execute(
            """
            INSERT INTO Venta (precio_final, tipo_pago, id_moto, id_cliente, id_empleado)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_venta
            """,
            (venta.precio_final, venta.tipo_pago, venta.id_moto,
             venta.id_cliente, venta.id_empleado)
        ).fetchone()

        nuevo_id = row["id_venta"]
        venta.id_venta = nuevo_id

        if venta.financiacion:
            venta.financiacion.id_venta = nuevo_id
            FinanciacionDAO.insertar(conn, venta.financiacion)

        MotoDAO.actualizar_estado(venta.id_moto, "vendida")  # sigue en Mongo

        return nuevo_id

    @staticmethod
    def eliminar(conn: ConexionPostgres, id_venta: int) -> None:
        conn.execute(
            "DELETE FROM Venta WHERE id_venta = %s",
            (id_venta,)
        )