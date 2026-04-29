from typing import Optional, List

from peewee import Model, AutoField, CharField, DoesNotExist

from db.gestor_conexiones import ConexionSQLite3
from model.VO.EmpleadoVO import EmpleadoVO


class _EmpleadoModel(Model):
    id_empleado = AutoField(column_name='id_empleado')
    nombre      = CharField(column_name='nombre')
    apellido    = CharField(column_name='apellido')
    rol         = CharField(column_name='rol')
    email       = CharField(column_name='email')

    class Meta:
        table_name = 'Empleado'

# Helper para convertir un registro de peewee a vo
def _a_vo(fila: _EmpleadoModel) -> EmpleadoVO:
    return EmpleadoVO(
        id_empleado=fila.id_empleado,
        nombre=fila.nombre,
        apellido=fila.apellido,
        rol=fila.rol,
        email=fila.email,
    )

# Usa Peewee porque Empleado es tabla plana, sin joins ni relaciones complejas.
class EmpleadoDAO:

    @staticmethod
    def obtener_por_id(conexion: ConexionSQLite3,
                       id_empleado: int) -> Optional[EmpleadoVO]:
        try:
            with _EmpleadoModel.bind_ctx(conexion.db_peewee):
                return _a_vo(_EmpleadoModel.get_by_id(id_empleado))
        except DoesNotExist:
            return None

    @staticmethod
    def listar(conexion: ConexionSQLite3) -> List[EmpleadoVO]:
        with _EmpleadoModel.bind_ctx(conexion.db_peewee):
            return [_a_vo(f) for f in _EmpleadoModel.select()]

    @staticmethod
    def listar_por_rol(conexion: ConexionSQLite3,
                       rol: str) -> List[EmpleadoVO]:
        with _EmpleadoModel.bind_ctx(conexion.db_peewee):
            return [
                _a_vo(f)
                for f in _EmpleadoModel.select()
                                       .where(_EmpleadoModel.rol == rol)
            ]