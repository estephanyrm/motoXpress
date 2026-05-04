from typing import List, Optional

from db.gestor_conexiones import connection_factory
from model.DAO.CategoriaDAO import CategoriaDAO
from model.VO.CategoriaVO import CategoriaVO


class CategoriaService:

    def listar_todas(self) -> List[CategoriaVO]:
        with connection_factory() as conexion:
            return CategoriaDAO.listar_todas(conexion)

    def obtener_por_id(self, id_categoria: int) -> Optional[CategoriaVO]:
        with connection_factory() as conexion:
            return CategoriaDAO.obtener_por_id(conexion, id_categoria)
