from typing import Optional

from db.gestor_conexiones import ConexionSQLite3

from model.DAO.VentaDAO import VentaDAO
from model.DAO.MotoDAO import MotoDAO
from model.DAO.FinanciacionDAO import FinanciacionDAO

from model.VO.VentaVO import VentaVO
from model.VO.FinanciacionVO import FinanciacionVO


class RegistrarVentaCommand:

    def __init__(self, venta: VentaVO,
                 financiacion: Optional[FinanciacionVO] = None):
        if financiacion is not None:
            venta.financiacion = financiacion

        self._venta = venta
        # Estado guardado durante execute() para poder revertir
        self._venta_id: Optional[int] = None
        self._moto_estado_anterior: Optional[str] = None
        self._financiacion_id: Optional[int] = None

    def execute(self, conn: ConexionSQLite3) -> None:
        # 1. Guarda estado previo de la moto (necesario para undo)
        moto = MotoDAO.obtener_por_id(conn, self._venta.id_moto)
        if moto is None:
            raise ValueError("Moto no encontrada.")
        self._moto_estado_anterior = moto.estado

        # 2. VentaDAO.insertar maneja todo: INSERT Venta + INSERT Financiacion + UPDATE Moto
        self._venta_id = VentaDAO.insertar(conn, self._venta)

        # 3. Guarda el id de la financiacion creada para poder eliminarla en undo
        if self._venta.financiacion:
            fin = FinanciacionDAO.obtener_por_venta(conn, self._venta_id)
            if fin:
                self._financiacion_id = fin.id_financiacion

    def undo(self, conn: ConexionSQLite3) -> None:
        if self._venta_id is None:
            raise RuntimeError("No se puede deshacer: el comando no ha sido ejecutado.")

        # Elimina financiación primero (restricción FK)
        if self._financiacion_id is not None:
            FinanciacionDAO.eliminar(conn, self._financiacion_id)

        # Elimina la venta
        VentaDAO.eliminar(conn, self._venta_id)

        # Restaura el estado anterior de la moto
        MotoDAO.actualizar_estado(conn, self._venta.id_moto,
                                  self._moto_estado_anterior)
