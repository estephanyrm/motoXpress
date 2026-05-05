from typing import List, Optional

from db.gestor_conexiones import connection_factory
from model.DAO.ClienteDAO import ClienteDAO
from model.VO.ClienteVO import ClienteVO


class ClienteService:

    def listar(self) -> List[ClienteVO]:
        with connection_factory() as conn:
            return ClienteDAO.listar(conn)

    def obtener_por_id(self, id_cliente: int) -> Optional[ClienteVO]:
        with connection_factory() as conn:
            return ClienteDAO.obtener_por_id(conn, id_cliente)

    def buscar_por_cedula(self, cedula: str) -> Optional[ClienteVO]:
        with connection_factory() as conn:
            return ClienteDAO.buscar_por_cedula(conn, cedula)

    def registrar(self, cliente: ClienteVO) -> int:
        if not cliente.nombre or not cliente.apellido or not cliente.cedula:
            raise ValueError("Nombre, apellido y cédula son obligatorios.")

        with connection_factory() as conn:
            if ClienteDAO.buscar_por_cedula(conn, cliente.cedula) is not None:
                raise ValueError(
                    f"Ya existe un cliente registrado con cédula '{cliente.cedula}'."
                )
            return ClienteDAO.insertar(conn, cliente)
