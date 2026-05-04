from typing import Optional, List

from peewee import Model, AutoField, CharField, TextField, DoesNotExist

from db.gestor_conexiones import ConexionSQLite3
from model.VO.CategoriaVO import CategoriaVO


class _CategoriaModel(Model):
    id_categoria = AutoField(column_name='id_categoria')
    nombre       = CharField(column_name='nombre')
    descripcion  = TextField(column_name='descripcion', null=True)

    class Meta:
        table_name = 'Categoria'


def _a_vo(fila: _CategoriaModel) -> CategoriaVO:
    return CategoriaVO(
        id_categoria=fila.id_categoria,
        nombre=fila.nombre,
        descripcion=fila.descripcion,
    )

# Usamos Peewee: Categoria es una tabla plana sin joins.
class CategoriaDAO:

    @staticmethod
    def listar_todas(conexion: ConexionSQLite3) -> List[CategoriaVO]:
        with _CategoriaModel.bind_ctx(conexion.db_peewee):
            return [_a_vo(f) for f in _CategoriaModel.select()]

    @staticmethod
    def obtener_por_id(conexion: ConexionSQLite3,
                       id_categoria: int) -> Optional[CategoriaVO]:
        try:
            with _CategoriaModel.bind_ctx(conexion.db_peewee):
                return _a_vo(_CategoriaModel.get_by_id(id_categoria))
        except DoesNotExist:
            return None 
