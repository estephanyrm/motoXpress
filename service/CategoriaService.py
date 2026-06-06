from typing import List, Optional
from mongo.model.DAO.CategoriaDAO import CategoriaDAO
from mongo.model.VO.CategoriaDocumento import CategoriaDocumento


class CategoriaService:

    def listar_todas(self) -> List[CategoriaDocumento]:
        return CategoriaDAO.listar_todas()

    def obtener_por_id(self, id_categoria: int) -> Optional[CategoriaDocumento]:
        return CategoriaDAO.obtener_por_id(id_categoria)

    def crear(self, nombre: str, descripcion: str = None) -> int:
        return CategoriaDAO.insertar(nombre, descripcion)

    def actualizar(self, id_categoria: int, nombre: str, descripcion: str = None) -> None:
        CategoriaDAO.actualizar(id_categoria, nombre, descripcion)

    def eliminar(self, id_categoria: int) -> None:
        CategoriaDAO.eliminar(id_categoria)
