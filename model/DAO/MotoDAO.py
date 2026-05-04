from typing import Optional, List
from sqlite3 import Cursor

from db.gestor_conexiones import ConexionSQLite3
from model.VO.MotoVO     import MotoVO
from model.VO.CategoriaVO import CategoriaVO
from model.DAO.MotoCategoriaDAO import MotoCategoriaDAO

class MotoDAO:
    # Carga lazy para listados generales
    @staticmethod
    def listar_disponibles(conexion: ConexionSQLite3) -> List[MotoVO]:
        sql: str = """
            SELECT id_moto, vin, marca, modelo, anio,
                   precio, color, estado
            FROM   Moto
            WHERE  estado = 'disponible'
        """
        cursor: Cursor = conexion.execute(sql)

        motos: List[MotoVO] = []

        for fila in cursor:
            r = dict(fila)

            moto = MotoVO(
                id_moto=r['id_moto'],
                vin=r['vin'],
                marca=r['marca'],
                modelo=r['modelo'],
                anio=r['anio'],
                precio=r['precio'],
                color=r['color'],
                estado=r['estado']
            )

            id_moto_capturado = r['id_moto']
            moto._categorias_loader = lambda id_m=id_moto_capturado: MotoCategoriaDAO.listar_categorias_de_moto(conexion, id_m)

            motos.append(moto)

        return motos

    # Carga eager para detalle
    @staticmethod
    def obtener_por_id(conexion: ConexionSQLite3,
                       id_moto: int) -> Optional[MotoVO]:
        sql: str = """
            SELECT id_moto, vin, marca, modelo, anio,
                   precio, color, estado
            FROM   Moto
            WHERE  id_moto = ?
        """
        cursor: Cursor = conexion.execute(sql, (id_moto,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        r = dict(fila)
        categorias: List[CategoriaVO] = MotoCategoriaDAO.listar_categorias_de_moto(conexion, id_moto)

        moto = MotoVO(
            id_moto=r['id_moto'],
            vin=r['vin'],
            marca=r['marca'],
            modelo=r['modelo'],
            anio=r['anio'],
            precio=r['precio'],
            color=r['color'],
            estado=r['estado']
        )
        moto._categorias_cache = categorias

        return moto

    @staticmethod
    def insertar(conexion: ConexionSQLite3,
                 moto: MotoVO) -> int:

        sql: str = """
            INSERT INTO Moto (vin, marca, modelo, anio, precio, color, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor: Cursor = conexion.cursor()
        cursor.execute(sql, (
            moto.vin,
            moto.marca,
            moto.modelo,
            moto.anio,
            moto.precio,
            moto.color,
            moto.estado
        ))
        return cursor.lastrowid

    @staticmethod
    def actualizar_estado(conexion: ConexionSQLite3,
                          id_moto: int,
                          nuevo_estado: str) -> None:
        sql: str = "UPDATE Moto SET estado = ? WHERE id_moto = ?"
        conexion.execute(sql, (nuevo_estado, id_moto))
    @staticmethod
    def actualizar(conexion: ConexionSQLite3, moto: MotoVO) -> None:
        """Actualiza todos los campos de una moto existente."""
        sql: str = """
            UPDATE Moto
            SET vin=?, marca=?, modelo=?, anio=?, precio=?, color=?, estado=?
            WHERE id_moto = ?
        """
        conexion.execute(sql, (
            moto.vin,
            moto.marca,
            moto.modelo,
            moto.anio,
            moto.precio,
            moto.color,
            moto.estado,
            moto.id_moto,
        ))

    @staticmethod
    def buscar_por_vin(conexion: ConexionSQLite3, vin: str) -> Optional[MotoVO]:
        sql: str = "SELECT id_moto, vin, marca, modelo, anio, precio, color, estado FROM Moto WHERE vin = ?"
        fila = conexion.execute(sql, (vin,)).fetchone()
        if fila is None:
            return None
        r = dict(fila)
        return MotoVO(
            id_moto=r['id_moto'],
            vin=r['vin'],
            marca=r['marca'],
            modelo=r['modelo'],
            anio=r['anio'],
            precio=r['precio'],
            color=r['color'],
            estado=r['estado'],
        )