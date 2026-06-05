from typing import List, Optional

from postgres.db.postgres import ConexionPostgres
from postgres.model.DAO.ClienteDAO import ClienteDAO
from postgres.model.VO.ClienteVO import ClienteVO

_PG = ConexionPostgres(
    host="localhost", port="5433",
    dbname="motoxpress", user="root", password="2007"
)


class ClienteService:

    def listar(self) -> List[ClienteVO]:
        with _PG as conn:
            return ClienteDAO.listar(conn)

    def obtener_por_id(self, id_cliente: int) -> Optional[ClienteVO]:
        with _PG as conn:
            return ClienteDAO.obtener_por_id(conn, id_cliente)

    def buscar_por_cedula(self, cedula: str) -> Optional[ClienteVO]:
        with _PG as conn:
            return ClienteDAO.buscar_por_cedula(conn, cedula)

    def registrar(self, cliente: ClienteVO) -> int:
        if not cliente.nombre or not cliente.apellido or not cliente.cedula:
            raise ValueError("Nombre, apellido y cédula son obligatorios.")
        with _PG as conn:
            if ClienteDAO.buscar_por_cedula(conn, cliente.cedula):
                raise ValueError(f"Ya existe un cliente con cédula '{cliente.cedula}'.")
            return ClienteDAO.insertar(conn, cliente)
