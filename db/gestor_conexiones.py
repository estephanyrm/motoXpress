import sqlite3
from sqlite3 import Connection
from typing import Optional

from peewee import SqliteDatabase


class ConexionSQLite3:
    """
    Context manager para conexiones SQLite3.

    Uso:
        with connection_factory() as conn:
            conn.execute(sql, params)

    Al salir del bloque:
      - Sin error  → COMMIT
      - Con error  → ROLLBACK
      - Siempre    → cierra conn sqlite3 y peewee
    """

    def __init__(self, db_path: str):
        self._db_path = db_path
        self._conn: Optional[Connection] = None
        self.db_peewee: Optional[SqliteDatabase] = None

    def execute(self, sql: str, params=()):
        """Delegación directa al cursor de sqlite3."""
        return self._conn.execute(sql, params)

    def cursor(self):
        return self._conn.cursor()

    def __enter__(self) -> "ConexionSQLite3":
        self._conn = sqlite3.connect(self._db_path)
        self._conn.row_factory = sqlite3.Row          # acceso por nombre de columna

        self.db_peewee = SqliteDatabase(self._db_path)
        self.db_peewee.connect()

        return self                                  

    def __exit__(self, exc_type, exc_val, tb) -> bool:
        if exc_type is None:
            self._conn.commit()
        else:
            self._conn.rollback()

        self._conn.close()

        if self.db_peewee and not self.db_peewee.is_closed():
            self.db_peewee.close()

        return False   

_DB_PATH = "db/concesionario.db"


def connection_factory() -> ConexionSQLite3:
    return ConexionSQLite3(_DB_PATH)
