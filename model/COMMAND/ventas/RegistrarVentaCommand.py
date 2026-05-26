from typing import Optional

from model.DAO.VentaDAO import VentaDAO
from model.DAO.MotoDAO import MotoDAO
from model.DAO.FinanciacionDAO import FinanciacionDAO

from model.VO.VentaVO import VentaVO
from model.VO.FinanciacionVO import FinanciacionVO


class RegistrarVentaCommand:

    def __init__(
        self,
        venta: VentaVO,
        financiacion: Optional[FinanciacionVO] = None
    ):
        if financiacion is not None:
            venta.financiacion = financiacion

        self._venta = venta

        self._venta_id = None
        self._moto_estado_anterior = None
        self._financiacion_id = None

    def execute(self) -> None:

        moto = MotoDAO.obtener_por_id(
            self._venta.id_moto
        )

        if moto is None:
            raise ValueError("Moto no encontrada.")

        self._moto_estado_anterior = moto.estado

        self._venta_id = VentaDAO.insertar(
            self._venta
        )

        if self._venta.financiacion:

            fin = FinanciacionDAO.obtener_por_venta(
                self._venta_id
            )

            if fin:
                self._financiacion_id = fin.id_financiacion

    def undo(self) -> None:

        if self._venta_id is None:
            raise RuntimeError(
                "No se puede deshacer: el comando no ha sido ejecutado."
            )

        if self._financiacion_id is not None:
            FinanciacionDAO.eliminar(
                self._financiacion_id
            )

        VentaDAO.eliminar(self._venta_id)

        MotoDAO.actualizar_estado(
            self._venta.id_moto,
            self._moto_estado_anterior
        )