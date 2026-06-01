from typing import List, Optional

from model.DAO.EmpleadoDAO import EmpleadoDAO
from model.VO.EmpleadoVO import EmpleadoVO


class EmpleadoService:

    def listar(self) -> List[EmpleadoVO]:
        return EmpleadoDAO.listar()

    def listar_por_rol(self, rol: str) -> List[EmpleadoVO]:
        return EmpleadoDAO.listar_por_rol(rol)

    def obtener_por_id(self, id_empleado: int) -> Optional[EmpleadoVO]:
        return EmpleadoDAO.obtener_por_id(id_empleado)