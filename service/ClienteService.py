from typing import List, Optional

from model.DAO.ClienteDAO import ClienteDAO
from model.VO.ClienteVO import ClienteVO


class ClienteService:

    def listar(self) -> List[ClienteVO]:
        return ClienteDAO.listar()

    def obtener_por_id(self, id_cliente: int) -> Optional[ClienteVO]:
        return ClienteDAO.obtener_por_id(id_cliente)

    def buscar_por_cedula(self, cedula: str) -> Optional[ClienteVO]:
        return ClienteDAO.buscar_por_cedula(cedula)

    def registrar(self, cliente: ClienteVO) -> int:

        if not cliente.nombre or not cliente.apellido or not cliente.cedula:
            raise ValueError(
                "Nombre, apellido y cédula son obligatorios."
            )

        if ClienteDAO.buscar_por_cedula(cliente.cedula):
            raise ValueError(
                f"Ya existe un cliente registrado con cédula '{cliente.cedula}'."
            )

        return ClienteDAO.insertar(cliente)