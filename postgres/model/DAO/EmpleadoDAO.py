from typing import Optional, List

from postgres.db.postgres import ConexionPostgres
from postgres.model.VO.EmpleadoVO import EmpleadoVO


def _a_vo(row) -> Optional[EmpleadoVO]:
    if row is None:
        return None
    return EmpleadoVO(
        id_empleado=row["id_empleado"],
        nombre=row["nombre"],
        apellido=row["apellido"],
        rol=row["rol"],
        email=row["email"]
    )


class EmpleadoDAO:

    @staticmethod
    def obtener_por_id(conn: ConexionPostgres, id_empleado: int) -> Optional[EmpleadoVO]:
        row = conn.execute(
            "SELECT * FROM Empleado WHERE id_empleado = %s",
            (id_empleado,)
        ).fetchone()
        return _a_vo(row)

    @staticmethod
    def listar(conn: ConexionPostgres) -> List[EmpleadoVO]:
        rows = conn.execute(
            "SELECT * FROM Empleado ORDER BY id_empleado"
        ).fetchall()
        return [_a_vo(r) for r in rows]

    @staticmethod
    def listar_por_rol(conn: ConexionPostgres, rol: str) -> List[EmpleadoVO]:
        rows = conn.execute(
            "SELECT * FROM Empleado WHERE rol = %s ORDER BY id_empleado",
            (rol,)
        ).fetchall()
        return [_a_vo(r) for r in rows]

    @staticmethod
    def insertar(conn: ConexionPostgres, empleado: EmpleadoVO) -> int:
        row = conn.execute(
            """
            INSERT INTO Empleado (nombre, apellido, rol, email)
            VALUES (%s, %s, %s, %s)
            RETURNING id_empleado
            """,
            (empleado.nombre, empleado.apellido, empleado.rol, empleado.email)
        ).fetchone()
        return row["id_empleado"]
