#  insertar, obtener_por_id, listar_por_cliente, listar_por_periodo
from typing import Optional, List
from sqlite3 import Cursor

from db.gestor_conexiones import ConexionSQLite3
from model.VO.VentaVO      import VentaVO
from model.VO.ClienteVO    import ClienteVO
from model.VO.MotoVO       import MotoVO
from model.VO.EmpleadoVO   import EmpleadoVO
from model.VO.FinanciacionVO import FinanciacionVO

from model.DAO.ClienteDAO     import ClienteDAO
from model.DAO.MotoDAO        import MotoDAO
from model.DAO.EmpleadoDAO    import EmpleadoDAO
from model.DAO.FinanciacionDAO import FinanciacionDAO

class VentaDAO:
    # Carga eager y lazy segun el caso de uso
    @staticmethod
    def listar_por_cliente(conexion: ConexionSQLite3,
                           id_cliente: int) -> List[VentaVO]:
        sql: str = """
            SELECT v.id_venta,
                   v.fecha_venta,
                   v.precio_final,
                   v.tipo_pago,
                   v.id_cliente,
                   v.id_moto,
                   v.id_empleado,
                   m.vin,
                   m.marca,
                   m.modelo,
                   m.anio,
                   m.precio,
                   m.color,
                   m.estado
            FROM   Venta v
            JOIN   Moto  m ON v.id_moto = m.id_moto
            WHERE  v.id_cliente = ?
            ORDER  BY v.fecha_venta DESC
        """
        cursor: Cursor = conexion.execute(sql, (id_cliente,))

        ventas: List[VentaVO] = []

        for fila in cursor:
            r = dict(fila)
            moto = MotoVO(
                id_moto=r['id_moto'],
                vin=r['vin'],
                marca=r['marca'],
                modelo=r['modelo'],
                anio=r['anio'],
                precio=r['precio'],
                color=r['color'],
                estado=r['estado']
            )

            venta = VentaVO(
                id_venta=r['id_venta'],
                fecha_venta=r['fecha_venta'],
                precio_final=r['precio_final'],
                tipo_pago=r['tipo_pago'],
                id_cliente=r['id_cliente'],
                id_moto=r['id_moto'],
                id_empleado=r['id_empleado']
            )

            venta._moto_cache = moto

            # Financiacion: LAZY — loader inyectado, no se ejecuta todavía
            id_venta_capturado = r['id_venta']
            venta._financiacion_loader = lambda id_v=id_venta_capturado: FinanciacionDAO.obtener_por_venta(conexion, id_v)

            # Empleado: LAZY — solo si alguien accede a venta.empleado
            id_empleado_capturado = r['id_empleado']
            venta._empleado_loader = lambda id_e=id_empleado_capturado: EmpleadoDAO.obtener_por_id(conexion, id_e)

            ventas.append(venta)

        return ventas

    # Carga eager para obtener el detalle de una venta
    @staticmethod
    def obtener_por_id(conexion: ConexionSQLite3,
                       id_venta: int) -> Optional[VentaVO]:
        sql: str = """
            SELECT * FROM Venta WHERE id_venta = ?
        """
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
            id_empleado=r['id_empleado']
        )

        venta._cliente_cache     = ClienteDAO.obtener_por_id(conexion, r['id_cliente'])
        venta._moto_cache        = MotoDAO.obtener_por_id(conexion, r['id_moto'])
        venta._empleado_cache    = EmpleadoDAO.obtener_por_id(conexion, r['id_empleado'])
        venta._financiacion_cache = FinanciacionDAO.obtener_por_venta(conexion, r['id_venta'])

        return venta

    # Carga eager para reportes
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
                   v.id_moto,
                   v.id_empleado,
                   m.marca,
                   m.modelo,
                   m.color,
                   m.estado,
                   m.vin,
                   m.anio,
                   m.precio,
                   e.nombre    AS nombre_empleado,
                   e.apellido  AS apellido_empleado,
                   e.rol,
                   e.email     AS email_empleado
            FROM   Venta    v
            JOIN   Moto     m ON v.id_moto     = m.id_moto
            JOIN   Empleado e ON v.id_empleado = e.id_empleado
            WHERE  v.fecha_venta BETWEEN ? AND ?
            ORDER  BY v.fecha_venta
        """
        cursor: Cursor = conexion.execute(sql, (fecha_inicio, fecha_fin))

        ventas: List[VentaVO] = []

        for fila in cursor:
            r = dict(fila)

            moto = MotoVO(
                id_moto=r['id_moto'],
                vin=r['vin'],
                marca=r['marca'],
                modelo=r['modelo'],
                anio=r['anio'],
                precio=r['precio'],
                color=r['color'],
                estado=r['estado']
            )

            empleado = EmpleadoVO(
                id_empleado=r['id_empleado'],
                nombre=r['nombre_empleado'],
                apellido=r['apellido_empleado'],
                rol=r['rol'],
                email=r['email_empleado']
            )

            venta = VentaVO(
                id_venta=r['id_venta'],
                fecha_venta=r['fecha_venta'],
                precio_final=r['precio_final'],
                tipo_pago=r['tipo_pago'],
                id_cliente=r['id_cliente'],
                id_moto=r['id_moto'],
                id_empleado=r['id_empleado']
            )

            venta._moto_cache     = moto
            venta._empleado_cache = empleado

            ventas.append(venta)

        return ventas

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
            venta.id_empleado
        ))
        return cursor.lastrowid