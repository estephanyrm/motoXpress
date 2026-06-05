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
        self._financiacion = financiacion

    def execute(self) -> None:
        with _PG as conn:
            VentaDAO.insertar(conn, self._venta)

    def undo(self) -> None:
        if self._venta.id_venta:
            with _PG as conn:
                VentaDAO.eliminar(conn, self._venta.id_venta)
