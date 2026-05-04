from typing import Optional
from sqlite3 import Cursor

from db.gestor_conexiones import ConexionSQLite3
from model.VO.FinanciacionVO import FinanciacionVO


class FinanciacionDAO:
    @staticmethod
    def obtener_por_venta(conexion: ConexionSQLite3,
                          id_venta: int) -> Optional[FinanciacionVO]:

        sql: str = """
            SELECT id_financiacion, cuotas, interes, monto_cuota, id_venta
            FROM   Financiacion
            WHERE  id_venta = ?
        """
        cursor: Cursor = conexion.execute(sql, (id_venta,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        r = dict(fila)
        return FinanciacionVO(
            id_financiacion=r['id_financiacion'],
            cuotas=r['cuotas'],
            interes=r['interes'],
            monto_cuota=r['monto_cuota'],
            id_venta=r['id_venta']
        )

    @staticmethod
    def insertar(conexion: ConexionSQLite3,
                 financiacion: FinanciacionVO) -> int:

        sql: str = """
            INSERT INTO Financiacion (cuotas, interes, monto_cuota, id_venta)
            VALUES (?, ?, ?, ?)
        """
        cursor: Cursor = conexion.cursor()
        cursor.execute(sql, (
            financiacion.cuotas,
            financiacion.interes,
            financiacion.monto_cuota,
            financiacion.id_venta
        ))
        return cursor.lastrowid
    
    @staticmethod
    def eliminar(conexion: ConexionSQLite3, id_financiacion: int) -> None:
        """Elimina una financiación por su PK. Usado por el undo del Command."""
        conexion.execute("DELETE FROM Financiacion WHERE id_financiacion = ?", (id_financiacion,))