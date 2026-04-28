from typing import Optional, List
from sqlite3 import Cursor

from db.gestor_conexiones import ConexionSQLite3
from model.VO.CategoriaVO import CategoriaVO

# Modelo Peewee definido UNA SOLA VEZ a nivel de módulo.
# Si se define dentro del método, Python recrea la clase en cada
# llamada y Peewee lanza warnings de "tabla ya registrada".
# bind_ctx() le asigna la BD en cada llamada sin tocar el modelo global.

try:
    from peewee import SqliteDatabase, Model, AutoField, CharField, TextField
    _PEEWEE_DISPONIBLE = True

    class _CategoriaModel(Model):
        id_categoria = AutoField()
        nombre       = CharField()
        descripcion  = TextField(null=True)

        class Meta:
            table_name = 'Categoria'

except ImportError:
    _PEEWEE_DISPONIBLE = False
    _CategoriaModel    = None


class CategoriaDAO:

    @staticmethod
    def listar_todas(conexion: ConexionSQLite3) -> List[CategoriaVO]:
        # Sin lazy: CategoriaVO no tiene relaciones hacia ninguna
        # otra entidad. 10 registros estáticos, se necesitan completos siempre.

        if _PEEWEE_DISPONIBLE:
            db_peewee = SqliteDatabase(conexion.db_path)
            db_peewee.connect()
            try:
                with _CategoriaModel.bind_ctx(db_peewee):
                    return [
                        CategoriaVO(
                            id_categoria=fila.id_categoria,
                            nombre=fila.nombre,
                            descripcion=fila.descripcion
                        )
                        for fila in _CategoriaModel.select()
                    ]
            finally:
                db_peewee.close()

        # Fallback manual: usa la conexión del context manager
        sql: str = "SELECT * FROM Categoria"
        cursor: Cursor = conexion.execute(sql)

        return [
            CategoriaVO(
                id_categoria=dict(fila)['id_categoria'],
                nombre=dict(fila)['nombre'],
                descripcion=dict(fila)['descripcion']
            )
            for fila in cursor
        ]

    @staticmethod
    def obtener_por_id(conexion: ConexionSQLite3,
                       id_categoria: int) -> Optional[CategoriaVO]:

        if _PEEWEE_DISPONIBLE:
            from peewee import DoesNotExist
            db_peewee = SqliteDatabase(conexion.db_path)
            db_peewee.connect()
            try:
                with _CategoriaModel.bind_ctx(db_peewee):
                    try:
                        fila = _CategoriaModel.get_by_id(id_categoria)
                        return CategoriaVO(
                            id_categoria=fila.id_categoria,
                            nombre=fila.nombre,
                            descripcion=fila.descripcion
                        )
                    except DoesNotExist:
                        return None
            finally:
                db_peewee.close()

        # Fallback manual
        sql: str = "SELECT * FROM Categoria WHERE id_categoria = ?"
        cursor: Cursor = conexion.execute(sql, (id_categoria,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        r = dict(fila)
        return CategoriaVO(
            id_categoria=r['id_categoria'],
            nombre=r['nombre'],
            descripcion=r['descripcion']
        )