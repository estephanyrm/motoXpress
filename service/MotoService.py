from typing import List, Optional

from db.gestor_conexiones import connection_factory
from model.DAO.MotoDAO import MotoDAO
from model.DAO.MotoCategoriaDAO import MotoCategoriaDAO
from model.VO.MotoVO import MotoVO

_ESTADOS_VALIDOS = {'disponible', 'vendida', 'reservada'}


class MotoService:

    def listar_disponibles(self) -> List[MotoVO]:
        with connection_factory() as conexion:
            return MotoDAO.listar_disponibles(conexion)

    def obtener_detalle(self, id_moto: int) -> Optional[MotoVO]:
        """Carga eager: retorna la moto con sus categorías ya pobladas."""
        with connection_factory() as conexion:
            return MotoDAO.obtener_por_id(conexion, id_moto)

    def registrar(self, moto: MotoVO,
                  ids_categorias: Optional[List[int]] = None) -> int:
        """
        Inserta una moto nueva y le asigna categorías opcionales.
        Regla de negocio: el VIN debe ser único en el sistema.
        Retorna el id generado.
        """
        with connection_factory() as conexion:
            duplicado = MotoDAO.buscar_por_vin(conexion, moto.vin)
            if duplicado is not None:
                raise ValueError(f"Ya existe una moto registrada con VIN '{moto.vin}'.")

            id_nuevo = MotoDAO.insertar(conexion, moto)

            if ids_categorias:
                for id_cat in ids_categorias:
                    MotoCategoriaDAO.asignar(conexion, id_nuevo, id_cat)

            return id_nuevo

    def cambiar_estado(self, id_moto: int, nuevo_estado: str) -> None:
        """
        Cambia el estado de una moto.
        Reglas de negocio:
          - El estado debe ser uno de los valores permitidos.
          - La moto debe existir.
        """
        if nuevo_estado not in _ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado '{nuevo_estado}' no válido. "
                f"Valores permitidos: {_ESTADOS_VALIDOS}"
            )

        with connection_factory() as conexion:
            moto = MotoDAO.obtener_por_id(conexion, id_moto)
            if moto is None:
                raise ValueError(f"No existe ninguna moto con id {id_moto}.")
            MotoDAO.actualizar_estado(conexion, id_moto, nuevo_estado)
