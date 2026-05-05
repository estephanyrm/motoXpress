from typing import Optional, List
from sqlite3 import Cursor

from db.gestor_conexiones import ConexionSQLite3
from model.VO.VentaVO import VentaVO
from model.VO.MotoVO import MotoVO

from model.DAO.ClienteDAO import ClienteDAO
from model.DAO.MotoDAO import MotoDAO
from model.DAO.EmpleadoDAO import EmpleadoDAO
from model.DAO.FinanciacionDAO import FinanciacionDAO


class VentaDAO:
    # Carga eager de moto y venta, carga lazy de financiacion
    @staticmethod
    def listar_por_cliente(conexion: ConexionSQLite3,
                           id_cliente: int) -> List[VentaVO]:
        sql: str = """
            SELECT v.id_venta,
                   v.fecha_venta,
                   v.precio_final,
                   v.tipo_pago,
                   v.id_cliente,
                   v.id_moto      AS v_id_moto,
                   v.id_empleado,
                   m.id_moto      AS m_id_moto,
                   m.vin, m.marca, m.modelo,
                   m.anio, m.precio, m.color, m.estado
            FROM   Venta v
            JOIN   Moto  m ON v.id_moto = m.id_moto
            WHERE  v.id_cliente = ?
        """
        cursor: Cursor = conexion.execute(sql, (id_cliente,))
        ventas: List[VentaVO] = []

        for fila in cursor:
            r = dict(fila)

            moto = MotoVO(
                id_moto=r['m_id_moto'],
                vin=r['vin'],
                marca=r['marca'],
                modelo=r['modelo'],
                anio=r['anio'],
                precio=r['precio'],
                color=r['color'],
                estado=r['estado'],
            )

            venta = VentaVO(
                id_venta=r['id_venta'],
                fecha_venta=r['fecha_venta'],
                precio_final=r['precio_final'],
                tipo_pago=r['tipo_pago'],
                id_cliente=r['id_cliente'],
                id_moto=r['v_id_moto'],
                id_empleado=r['id_empleado'],
            )
            venta._moto_cache = moto

            id_v = r['id_venta']
            venta._financiacion_loader = (
                lambda id_v=id_v: FinanciacionDAO.obtener_por_venta(conexion, id_v)
            )

            ventas.append(venta)

        return ventas

    # Carga Eager de Moto y Venta para optimizar el listado por fechas.
    # Carga Lazy de Financiación para evitar consultas innecesarias en reportes masivos.
    @staticmethod
    def listar_por_periodo(conexion: ConexionSQLite3,
                           fecha_inicio: str,
                           fecha_fin: str) -> List[VentaVO]:
        sql: str = """
            SELECT v.id_venta,
                   v.fecha_venta,
                   v.precio_final,
                   v.tipo_pago,
                   v.id_cliente,
                   v.id_moto      AS v_id_moto,
                   v.id_empleado,
                   m.id_moto      AS m_id_moto,
                   m.vin, m.marca, m.modelo,
                   m.anio, m.precio, m.color, m.estado
            FROM   Venta v
            JOIN   Moto  m ON v.id_moto = m.id_moto
            WHERE  v.fecha_venta BETWEEN ? AND ?
            ORDER  BY v.fecha_venta DESC
        """
        cursor: Cursor = conexion.execute(sql, (fecha_inicio, fecha_fin))
        ventas: List[VentaVO] = []

        for fila in cursor:
            r = dict(fila)

            moto = MotoVO(
                id_moto=r['m_id_moto'],
                vin=r['vin'],
                marca=r['marca'],
                modelo=r['modelo'],
                anio=r['anio'],
                precio=r['precio'],
                color=r['color'],
                estado=r['estado'],
            )

            venta = VentaVO(
                id_venta=r['id_venta'],
                fecha_venta=r['fecha_venta'],
                precio_final=r['precio_final'],
                tipo_pago=r['tipo_pago'],
                id_cliente=r['id_cliente'],
                id_moto=r['v_id_moto'],
                id_empleado=r['id_empleado'],
            )
            venta._moto_cache = moto

            id_v = r['id_venta']
            venta._financiacion_loader = (
                lambda id_v=id_v: FinanciacionDAO.obtener_por_venta(conexion, id_v)
            )

            ventas.append(venta)

        return ventas

    # Carga Eager completa para obtener toda la información de una venta individual, optimizando consultas posteriores a través de caching interno.
    @staticmethod
    def obtener_por_id(conexion: ConexionSQLite3,
                       id_venta: int) -> Optional[VentaVO]:
        sql: str = "SELECT * FROM Venta WHERE id_venta = ?"
        cursor: Cursor = conexion.execute(sql, (id_venta,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        r = dict(fila)

        venta = VentaVO(
            id_venta=r['id_venta'],
            fecha_venta=r['fecha_venta'],
            precio_final=r['precio_final'],
            tipo_pago=r['tipo_pago'],
            id_cliente=r['id_cliente'],
            id_moto=r['id_moto'],
            id_empleado=r['id_empleado'],
        )

        # Eager loading completo para el detalle individual
        venta._cliente_cache  = ClienteDAO.obtener_por_id(conexion, r['id_cliente'])
        venta._moto_cache     = MotoDAO.obtener_por_id(conexion, r['id_moto'])
        venta._empleado_cache = EmpleadoDAO.obtener_por_id(conexion, r['id_empleado'])
        venta.financiacion    = FinanciacionDAO.obtener_por_venta(conexion, r['id_venta'])

        return venta

    @staticmethod
    def insertar(conexion: ConexionSQLite3,
                 venta: VentaVO) -> int:
        sql: str = """
            INSERT INTO Venta (fecha_venta, precio_final, tipo_pago,
                               id_cliente, id_moto, id_empleado)
            VALUES (date('now'), ?, ?, ?, ?, ?)
        """
        cursor: Cursor = conexion.cursor()
        cursor.execute(sql, (
            venta.precio_final,
            venta.tipo_pago,
            venta.id_cliente,
            venta.id_moto,
            venta.id_empleado,
        ))

        id_venta = cursor.lastrowid
        venta.id_venta = id_venta

        if venta.financiacion:
            venta.financiacion.id_venta = id_venta
            FinanciacionDAO.insertar(conexion, venta.financiacion)

        MotoDAO.actualizar_estado(conexion, venta.id_moto, 'vendida')

        return id_venta

    @staticmethod
    def eliminar(conexion: ConexionSQLite3, id_venta: int) -> None:
        conexion.execute("DELETE FROM Venta WHERE id_venta = ?", (id_venta,))
