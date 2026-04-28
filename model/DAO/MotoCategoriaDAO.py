from typing import List
from sqlite3 import Cursor

from db.gestor_conexiones import ConexionSQLite3
from model.VO.CategoriaVO import CategoriaVO

class MotoCategoriaDAO:
    # Carga eager para mostrar categorias en el detalle de la moto
    @staticmethod
    def listar_categorias_de_moto(conexion: ConexionSQLite3,
                                   id_moto: int) -> List[CategoriaVO]:

        sql: str = """
            SELECT c.id_categoria, c.nombre, c.descripcion
            FROM   Categoria c
            JOIN   MotoCategoria mc ON c.id_categoria = mc.id_categoria
            WHERE  mc.id_moto = ?
        """
        cursor: Cursor = conexion.execute(sql, (id_moto,))

        return [
            CategoriaVO(
                id_categoria=dict(f)['id_categoria'],
                nombre=dict(f)['nombre'],
                descripcion=dict(f)['descripcion']
            )
            for f in cursor
        ]
    
    @staticmethod
    def asignar(conexion: ConexionSQLite3,
                id_moto: int,
                id_categoria: int) -> None:
        sql: str = """
            INSERT OR IGNORE INTO MotoCategoria (id_moto, id_categoria)
            VALUES (?, ?)
        """
        conexion.execute(sql, (id_moto, id_categoria))

    @staticmethod
    def remover(conexion: ConexionSQLite3,
                id_moto: int,
                id_categoria: int) -> None:

        sql: str = """
            DELETE FROM MotoCategoria
            WHERE id_moto = ? AND id_categoria = ?
        """
        conexion.execute(sql, (id_moto, id_categoria))