from typing import Optional, List

from postgres.db.postgres import ConexionPostgres
from postgres.model.VO.VentaVO import VentaVO
from postgres.model.DAO.ClienteDAO import ClienteDAO
from postgres.model.DAO.EmpleadoDAO import EmpleadoDAO
from postgres.model.DAO.FinanciacionDAO import FinanciacionDAO
from mongo.model.DAO.MotoDAO import MotoDAO


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
    def listar_todas(conn: ConexionPostgres) -> List[VentaVO]:
        rows = conn.execute(
            "SELECT * FROM Venta ORDER BY fecha_venta DESC"
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
    def insertar(conn: ConexionPostgres, venta: VentaVO) -> int:
        from datetime import datetime, timezone, timedelta
        # UTC-5 Colombia — evita que PostgreSQL (UTC) registre "mañana"
        tz_colombia = timezone(timedelta(hours=-5))
        fecha_hoy = datetime.now(tz_colombia).date()

        row = conn.execute(
            """
            INSERT INTO Venta (fecha_venta, precio_final, tipo_pago, id_moto, id_cliente, id_empleado)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_venta
            """,
            (fecha_hoy, venta.precio_final, venta.tipo_pago, venta.id_moto,
             venta.id_cliente, venta.id_empleado)
        ).fetchone()

        nuevo_id = row["id_venta"]
        venta.id_venta = nuevo_id

        if venta.financiacion:
            venta.financiacion.id_venta = nuevo_id
            FinanciacionDAO.insertar(conn, venta.financiacion)

        MotoDAO.actualizar_estado(venta.id_moto, "vendida")
        return nuevo_id

    @staticmethod
    def eliminar(conn: ConexionPostgres, id_venta: int) -> None:
        conn.execute(
            "DELETE FROM Venta WHERE id_venta = %s",
            (id_venta,)
        )