from db.gestor_conexiones import ConexionSQLite3

from model.DAO.VentaDAO import VentaDAO
from model.DAO.MotoDAO import MotoDAO
from model.DAO.FinanciacionDAO import FinanciacionDAO

from model.VO.VentaVO import VentaVO


class RegistrarVentaCommand:

    def __init__(self, venta: VentaVO):
        self.venta = venta
        self.venta_id = None
        self.moto_estado_anterior = None
        self.financiacion = None

    def execute(self, conn: ConexionSQLite3):

        if self.venta_id is None:
            moto = MotoDAO.obtener_por_id(conn, self.venta.id_moto)
            self.moto_estado_anterior = moto.estado

            self.venta_id = VentaDAO.insertar(conn, self.venta)
            self.venta.id_venta = self.venta_id

            moto.estado = "vendida"
            MotoDAO.actualizar(conn, moto)

            if self.venta.es_financiada:
                self.financiacion = self.venta.financiacion

        else:
            self.venta_id = VentaDAO.insertar(conn, self.venta)

    def undo(self, conn: ConexionSQLite3):
        VentaDAO.eliminar(conn, self.venta_id)

        moto = MotoDAO.obtener_por_id(conn, self.venta.id_moto)
        moto.estado = self.moto_estado_anterior
        MotoDAO.actualizar(conn, moto)

        if self.financiacion is not None:
            FinanciacionDAO.eliminar(conn, self.financiacion.id_financiacion)