from typing import List, Optional

from db.gestor_conexiones import connection_factory
from model.DAO.ClienteDAO import ClienteDAO
from model.VO.ClienteVO import ClienteVO


class ClienteService:

    def listar(self) -> List[ClienteVO]:
        with connection_factory() as conexion:
            return ClienteDAO.listar(conexion)

    def obtener_por_id(self, id_cliente: int) -> Optional[ClienteVO]:
        with connection_factory() as conexion:
            return ClienteDAO.obtener_por_id(conexion, id_cliente)

    def buscar_por_cedula(self, cedula: str) -> Optional[ClienteVO]:
        with connection_factory() as conexion:
            return ClienteDAO.buscar_por_cedula(conexion, cedula)

    def registrar(self, cliente: ClienteVO) -> int:
        """
        Inserta un cliente nuevo.
        Reglas de negocio:
          - La cédula debe ser única en el sistema.
          - Nombre, apellido y cédula son obligatorios.
        Retorna el id generado.
        """
        if not cliente.nombre or not cliente.apellido or not cliente.cedula:
            raise ValueError("Nombre, apellido y cédula son obligatorios.")

        with connection_factory() as conexion:
            duplicado = ClienteDAO.buscar_por_cedula(conexion, cliente.cedula)
            if duplicado is not None:
                raise ValueError(
                    f"Ya existe un cliente registrado con cédula '{cliente.cedula}'."
                )
            return ClienteDAO.insertar(conexion, cliente)
