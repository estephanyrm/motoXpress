from typing import Optional, List

from peewee import Model, AutoField, CharField, DateTimeField, DoesNotExist

from db.gestor_conexiones import ConexionSQLite3
from model.VO.ClienteVO import ClienteVO

class _ClienteModel(Model):
    id_cliente     = AutoField(column_name='id_cliente')
    nombre         = CharField(column_name='nombre')
    apellido       = CharField(column_name='apellido')
    cedula         = CharField(column_name='cedula')
    telefono       = CharField(column_name='telefono')
    email          = CharField(column_name='email')
    fecha_registro = DateTimeField(column_name='fecha_registro', null=True)

    class Meta:
        table_name = 'Cliente'

# Helper para convertir un registro peewe a VO
def _a_vo(fila: _ClienteModel) -> ClienteVO:
    return ClienteVO(
        id_cliente=fila.id_cliente,
        nombre=fila.nombre,
        apellido=fila.apellido,
        cedula=fila.cedula,
        telefono=fila.telefono,
        email=fila.email,
        fecha_registro=fila.fecha_registro,
    )


# Usa Peewee porque Cliente tiene operaciones CRUD simples sobre una sola tabla
class ClienteDAO:
    @staticmethod
    def obtener_por_id(conexion: ConexionSQLite3,
                       id_cliente: int) -> Optional[ClienteVO]:
        try:
            with _ClienteModel.bind_ctx(conexion.db_peewee):
                return _a_vo(_ClienteModel.get_by_id(id_cliente))
        except DoesNotExist:
            return None

    @staticmethod
    def listar(conexion: ConexionSQLite3) -> List[ClienteVO]:
        with _ClienteModel.bind_ctx(conexion.db_peewee):
            return [_a_vo(f) for f in _ClienteModel.select()]

    @staticmethod
    def buscar_por_cedula(conexion: ConexionSQLite3,
                          cedula: str) -> Optional[ClienteVO]:
        with _ClienteModel.bind_ctx(conexion.db_peewee):
            fila = _ClienteModel.get_or_none(_ClienteModel.cedula == cedula)
            return _a_vo(fila) if fila else None

    @staticmethod
    def insertar(conexion: ConexionSQLite3,
                 cliente: ClienteVO) -> int:
        with _ClienteModel.bind_ctx(conexion.db_peewee):
            registro = _ClienteModel.create(
                nombre=cliente.nombre,
                apellido=cliente.apellido,
                cedula=cliente.cedula,
                telefono=cliente.telefono,
                email=cliente.email,
            )
            return registro.id_cliente