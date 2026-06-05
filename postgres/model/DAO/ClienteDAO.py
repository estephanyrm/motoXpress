from typing import Optional, List

from postgres.db.postgres import ConexionPostgres
from postgres.model.VO.ClienteVO import ClienteVO


def _a_vo(row) -> Optional[ClienteVO]:
    if row is None:
        return None
    return ClienteVO(
        id_cliente=row["id_cliente"],
        nombre=row["nombre"],
        apellido=row["apellido"],
        cedula=row["cedula"],
        telefono=row["telefono"],
        email=row["email"],
        fecha_registro=row["fecha_registro"]
    )


class ClienteDAO:

    @staticmethod
    def listar(conn: ConexionPostgres) -> List[ClienteVO]:
        rows = conn.execute(
            "SELECT * FROM Cliente ORDER BY id_cliente"
        ).fetchall()
        return [_a_vo(r) for r in rows]

    @staticmethod
    def obtener_por_id(conn: ConexionPostgres, id_cliente: int) -> Optional[ClienteVO]:
        row = conn.execute(
            "SELECT * FROM Cliente WHERE id_cliente = %s",
            (id_cliente,)
        ).fetchone()
        return _a_vo(row)

    @staticmethod
    def buscar_por_cedula(conn: ConexionPostgres, cedula: str) -> Optional[ClienteVO]:
        row = conn.execute(
            "SELECT * FROM Cliente WHERE cedula = %s",
            (cedula,)
        ).fetchone()
        return _a_vo(row)

    @staticmethod
    def insertar(conn: ConexionPostgres, cliente: ClienteVO) -> int:
        row = conn.execute(
            """
            INSERT INTO Cliente (nombre, apellido, cedula, telefono, email, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)
            RETURNING id_cliente
            """,
            (cliente.nombre, cliente.apellido, cliente.cedula,
             cliente.telefono, cliente.email)
        ).fetchone()
        return row["id_cliente"]
