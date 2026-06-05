from typing import List, Optional

from postgres.db.postgres import ConexionPostgres
from postgres.model.DAO.EmpleadoDAO import EmpleadoDAO
from postgres.model.VO.EmpleadoVO import EmpleadoVO

_PG = ConexionPostgres(
    host="localhost", port="5433",
    dbname="motoxpress", user="root", password="2007"
)


class EmpleadoService:

    def listar(self) -> List[EmpleadoVO]:
        with _PG as conn:
            return EmpleadoDAO.listar(conn)

    def listar_por_rol(self, rol: str) -> List[EmpleadoVO]:
        with _PG as conn:
            return EmpleadoDAO.listar_por_rol(conn, rol)

    def obtener_por_id(self, id_empleado: int) -> Optional[EmpleadoVO]:
        with _PG as conn:
            return EmpleadoDAO.obtener_por_id(conn, id_empleado)
