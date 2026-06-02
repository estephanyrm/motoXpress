# model/DAO/FinanciacionDAO.py
from typing import Optional

from db.postgres import ConexionPostgres
from model.VO.FinanciacionVO import FinanciacionVO


def _a_vo(row) -> Optional[FinanciacionVO]:
    if row is None:
        return None
    return FinanciacionVO(
        id_financiacion=row["id_financiacion"],
        cuotas=row["cuotas"],
        interes=row["interes"],
        monto_cuota=row["monto_cuota"],
        id_venta=row["id_venta"]
    )


class FinanciacionDAO:

    @staticmethod
    def obtener_por_venta(conn: ConexionPostgres, id_venta: int) -> Optional[FinanciacionVO]:
        row = conn.execute(
            "SELECT * FROM Financiacion WHERE id_venta = %s",
            (id_venta,)
        ).fetchone()
        return _a_vo(row)

    @staticmethod
    def insertar(conn: ConexionPostgres, financiacion: FinanciacionVO) -> int:
        # Necesitamos fecha_venta porque Financiacion referencia
        # la clave compuesta (id_venta, fecha_venta) de la tabla Venta
        fecha = conn.execute(
            "SELECT fecha_venta FROM Venta WHERE id_venta = %s",
            (financiacion.id_venta,)
        ).fetchone()

        row = conn.execute(
            """
            INSERT INTO Financiacion (cuotas, interes, monto_cuota, id_venta, fecha_venta)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_financiacion
            """,
            (financiacion.cuotas, financiacion.interes, financiacion.monto_cuota,
             financiacion.id_venta, fecha["fecha_venta"])
        ).fetchone()
        return row["id_financiacion"]

    @staticmethod
    def eliminar(conn: ConexionPostgres, id_financiacion: int) -> None:
        conn.execute(
            "DELETE FROM Financiacion WHERE id_financiacion = %s",
            (id_financiacion,)
        )
        
        
        
        