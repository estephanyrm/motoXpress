from typing import Optional, List
from sqlite3 import Cursor

from db.gestor_conexiones import ConexionSQLite3
from model.VO.ClienteVO import ClienteVO

class ClienteDAO:
    # Carga eager para obtener el detalle de un cliente
    @staticmethod
    def obtener_por_id(conexion: ConexionSQLite3,
                       id_cliente: int) -> Optional[ClienteVO]:

        sql: str = "SELECT * FROM Cliente WHERE id_cliente = ?"
        cursor: Cursor = conexion.execute(sql, (id_cliente,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        r = dict(fila)
        return ClienteVO(
            id_cliente=r['id_cliente'],
            nombre=r['nombre'],
            apellido=r['apellido'],
            cedula=r['cedula'],
            telefono=r['telefono'],
            email=r['email'],
            fecha_registro=r['fecha_registro']
        )

    # Carga eager para obtener el cliente por cedula
    @staticmethod
    def obtener_por_cedula(conexion: ConexionSQLite3,
                           cedula: str) -> Optional[ClienteVO]:
        sql: str = "SELECT * FROM Cliente WHERE cedula = ?"
        cursor: Cursor = conexion.execute(sql, (cedula,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        r = dict(fila)
        return ClienteVO(
            id_cliente=r['id_cliente'],
            nombre=r['nombre'],
            apellido=r['apellido'],
            cedula=r['cedula'],
            telefono=r['telefono'],
            email=r['email'],
            fecha_registro=r['fecha_registro']
        )

    @staticmethod
    def insertar(conexion: ConexionSQLite3,
                 cliente: ClienteVO) -> int:

        sql: str = """
            INSERT INTO Cliente (nombre, apellido, cedula, telefono, email, fecha_registro)
            VALUES (?, ?, ?, ?, ?, date('now'))
        """
        cursor: Cursor = conexion.cursor()
        cursor.execute(sql, (
            cliente.nombre,
            cliente.apellido,
            cliente.cedula,
            cliente.telefono,
            cliente.email
        ))
        return cursor.lastrowid

    # Carga eager para listar clientes con orden por apellido
    @staticmethod
    def listar(conexion: ConexionSQLite3) -> List[ClienteVO]:

        sql: str = "SELECT * FROM Cliente ORDER BY apellido"
        cursor: Cursor = conexion.execute(sql)

        return [
            ClienteVO(
                id_cliente=dict(f)['id_cliente'],
                nombre=dict(f)['nombre'],
                apellido=dict(f)['apellido'],
                cedula=dict(f)['cedula'],
                telefono=dict(f)['telefono'],
                email=dict(f)['email'],
                fecha_registro=dict(f)['fecha_registro']
            )
            for f in cursor
        ]