from typing import Optional, List
from sqlite3 import Cursor

from db.gestor_conexiones import ConexionSQLite3
from model.VO.MotoVO import MotoVO
from model.VO.CategoriaVO import CategoriaVO
from model.DAO.MotoCategoriaDAO import MotoCategoriaDAO


class MotoDAO:
    @staticmethod
    def listar_disponibles(conexion: ConexionSQLite3) -> List[MotoVO]:
        sql: str = """
            SELECT id_moto, vin, marca, modelo, anio,
                   precio, color, estado
            FROM Moto
            WHERE estado = 'disponible'
        """
        cursor: Cursor = conexion.execute(sql)
        filas = cursor.fetchall()  # materializar antes de abrir nuevos cursores

        motos: List[MotoVO] = []

        for fila in filas:
            r = dict(fila)
            id_moto = r['id_moto']

            # Carga eager dentro de la misma conexion abierta.
            # El lazy loader (closure sobre conexion) falla porque la
            # conexion ya esta cerrada al momento de llamar cargar_categorias().
            categorias = MotoCategoriaDAO.listar_categorias_de_moto(conexion, id_moto)

            moto = MotoVO(
                id_moto=id_moto,
                vin=r['vin'],
                marca=r['marca'],
                modelo=r['modelo'],
                anio=r['anio'],
                precio=r['precio'],
                color=r['color'],
                estado=r['estado'],
                categorias=categorias,
            )

            motos.append(moto)

        return motos


    @staticmethod
    def obtener_por_id(conexion: ConexionSQLite3,
                       id_moto: int) -> Optional[MotoVO]:

        sql: str = """
            SELECT id_moto, vin, marca, modelo, anio,
                   precio, color, estado
            FROM Moto
            WHERE id_moto = ?
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
        moto.categorias = categorias

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
        sql: str = """
            SELECT id_moto, vin, marca, modelo, anio, precio, color, estado
            FROM Moto WHERE vin = ?
        """
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