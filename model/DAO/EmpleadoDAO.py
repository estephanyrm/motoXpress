from typing import Optional, List
from sqlite3 import Cursor

from db.gestor_conexiones import ConexionSQLite3
from model.VO.EmpleadoVO import EmpleadoVO

# Sin lazy: EmpleadoVO no tiene relaciones. 8 registros, cada fila autosuficiente.
# Peewee primario para lecturas simples. Modelo a nivel de módulo (una sola definición).

try:
    from peewee import SqliteDatabase, Model, AutoField, CharField
    _PEEWEE_DISPONIBLE = True

    class _EmpleadoModel(Model):
        id_empleado = AutoField()
        nombre      = CharField()
        apellido    = CharField()
        rol         = CharField()
        email       = CharField()

        class Meta:
            table_name = 'Empleado'

except ImportError:
    _PEEWEE_DISPONIBLE = False
    _EmpleadoModel     = None


class EmpleadoDAO:

    @staticmethod
    def obtener_por_id(conexion: ConexionSQLite3,
                       id_empleado: int) -> Optional[EmpleadoVO]:

        if _PEEWEE_DISPONIBLE:
            from peewee import DoesNotExist
            db_peewee = SqliteDatabase(conexion.db_path)
            db_peewee.connect()
            try:
                with _EmpleadoModel.bind_ctx(db_peewee):
                    try:
                        fila = _EmpleadoModel.get_by_id(id_empleado)
                        return EmpleadoVO(
                            id_empleado=fila.id_empleado,
                            nombre=fila.nombre,
                            apellido=fila.apellido,
                            rol=fila.rol,
                            email=fila.email
                        )
                    except DoesNotExist:
                        return None
            finally:
                db_peewee.close()

        # Fallback manual
        sql: str = "SELECT * FROM Empleado WHERE id_empleado = ?"
        cursor: Cursor = conexion.execute(sql, (id_empleado,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        r = dict(fila)
        return EmpleadoVO(
            id_empleado=r['id_empleado'],
            nombre=r['nombre'],
            apellido=r['apellido'],
            rol=r['rol'],
            email=r['email']
        )

    @staticmethod
    def listar(conexion: ConexionSQLite3) -> List[EmpleadoVO]:

        if _PEEWEE_DISPONIBLE:
            db_peewee = SqliteDatabase(conexion.db_path)
            db_peewee.connect()
            try:
                with _EmpleadoModel.bind_ctx(db_peewee):
                    return [
                        EmpleadoVO(
                            id_empleado=f.id_empleado,
                            nombre=f.nombre,
                            apellido=f.apellido,
                            rol=f.rol,
                            email=f.email
                        )
                        for f in _EmpleadoModel.select()
                    ]
            finally:
                db_peewee.close()

        # Fallback manual
        sql: str = "SELECT * FROM Empleado"
        cursor: Cursor = conexion.execute(sql)
        return [
            EmpleadoVO(
                id_empleado=dict(f)['id_empleado'],
                nombre=dict(f)['nombre'],
                apellido=dict(f)['apellido'],
                rol=dict(f)['rol'],
                email=dict(f)['email']
            )
            for f in cursor
        ]