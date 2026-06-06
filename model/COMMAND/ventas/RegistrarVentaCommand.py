from postgres.db.postgres import ConexionPostgres
from postgres.model.DAO.VentaDAO import VentaDAO
from postgres.model.VO.VentaVO import VentaVO
from postgres.model.VO.FinanciacionVO import FinanciacionVO
from typing import Optional

_PG = ConexionPostgres(
    host="localhost", port="5433",
    dbname="motoxpress", user="root", password="2007"
)

class RegistrarVentaCommand:

    def __init__(self, venta: VentaVO, financiacion: Optional[FinanciacionVO] = None):
        self._venta = venta
        self._venta_id  = None
        self._moto_estado_anterior = "disponible"
        self._financiacion_id = None

    def execute(self) -> None:
        with _PG as conn:
            VentaDAO.insertar(conn, self._venta)
        self._venta_id = self._venta.id_venta

    def undo(self) -> None:
        if self._venta.id_venta:
            with _PG as conn:
                VentaDAO.eliminar(conn, self._venta.id_venta)
            from mongo.model.DAO.MotoDAO import MotoDAO
            MotoDAO.actualizar_estado(self._venta.id_moto, self._moto_estado_anterior)
