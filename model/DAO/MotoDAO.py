from typing import Optional, List
from sqlite3 import Cursor

from db.gestor_conexiones import ConexionSQLite3

from model.VO.MotoVO import MotoVO
from model.VO.CategoriaVO import CategoriaVO

class MotoDAO:

    @staticmethod
    def obtener_motos(conexion: ConexionSQLite3)->List[MotoVO]:

        sql: str = """
            SELECT  m.ID_Moto, 
                    m.Marca,
                    m.Modelo, 
                    m.Precio, 
                    c.ID_Categoria,
                    c.Nombre_Categoria,
            FROM Moto m 
            JOIN Categoria c ON m.ID_Categoria = c.ID_Categoria
        """

        cursor: Cursor = conexion.execute(sql)

        motos: List[MotoVO] = []

        for registro in cursor:
            r = dict(registro)

            categoria = CategoriaVO(
                id_categoria=r['id_categoria'],
                nombre_categoria=r['nombre_categoria']
            )

            moto = MotoVO(
                id_moto=r['id_moto'],
                marca=r['marca'],
                modelo=r['modelo'],
                precio=r['precio'],
                categoria=categoria
            )

            motos.append(moto)

        return motos