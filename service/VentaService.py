from typing import List, Optional

from db.gestor_conexiones import connection_factory
from model.COMMAND.UndoRedoManager import UndoRedoManager
from model.COMMAND.ventas.RegistrarVentaCommand import RegistrarVentaCommand

from model.DAO.VentaDAO import VentaDAO
from model.DAO.MotoDAO import MotoDAO
from model.DAO.ClienteDAO import ClienteDAO
from model.DAO.EmpleadoDAO import EmpleadoDAO

from model.VO.VentaVO import VentaVO
from model.VO.FinanciacionVO import FinanciacionVO

_TIPOS_PAGO = {'contado', 'financiado', 'tarjeta'}


class VentaService:

    def __init__(self, undo_redo_manager: UndoRedoManager):
        self._undo_redo = undo_redo_manager

    def registrar(self,
                  venta: VentaVO,
                  financiacion: Optional[FinanciacionVO] = None) -> int:
        if venta.tipo_pago not in _TIPOS_PAGO:
            raise ValueError(
                f"Tipo de pago '{venta.tipo_pago}' no válido. "
                f"Permitidos: {_TIPOS_PAGO}"
            )

        if venta.tipo_pago == 'financiado':
            if financiacion is None:
                raise ValueError(
                    "Se requiere un plan de financiación cuando el tipo de pago es 'financiado'."
                )
            if not financiacion.cuotas or financiacion.cuotas <= 0:
                raise ValueError("El número de cuotas debe ser mayor a cero.")
            if financiacion.interes is None or financiacion.interes < 0:
                raise ValueError("El interés no puede ser negativo.")

        with connection_factory() as conn:
            if ClienteDAO.obtener_por_id(conn, venta.id_cliente) is None:
                raise ValueError(f"No existe cliente con id {venta.id_cliente}.")

            moto = MotoDAO.obtener_por_id(conn, venta.id_moto)
            if moto is None:
                raise ValueError(f"No existe moto con id {venta.id_moto}.")
            if moto.estado != 'disponible':
                raise ValueError(
                    f"La moto '{moto.marca} {moto.modelo}' no está disponible "
                    f"(estado actual: '{moto.estado}')."
                )

            if EmpleadoDAO.obtener_por_id(conn, venta.id_empleado) is None:
                raise ValueError(f"No existe empleado con id {venta.id_empleado}.")

            if venta.tipo_pago == 'financiado':
                financiacion.monto_cuota = round(
                    venta.precio_final * (1 + financiacion.interes / 100)
                    / financiacion.cuotas,
                    2
                )

            command = RegistrarVentaCommand(venta, financiacion)
            command.execute(conn)

        self._undo_redo.register(command)
        return venta.id_venta

    def deshacer_ultima_venta(self) -> bool:
        command = self._undo_redo.get_undo()
        if command is None:
            return False

        with connection_factory() as conn:
            command.undo(conn)
        self._undo_redo.push_redo(command)

        return True

    def rehacer_ultima_venta(self) -> bool:
        command = self._undo_redo.get_redo()
        if command is None:
            return False

        with connection_factory() as conn:
            command.execute(conn)
        self._undo_redo.push_undo(command)

        return True

    def puede_deshacer(self) -> bool:
        return self._undo_redo.tiene_undo()

    def puede_rehacer(self) -> bool:
        return self._undo_redo.tiene_redo()

    def obtener_detalle(self, id_venta: int) -> Optional[VentaVO]:
        # Eager loading: cliente, moto, empleado y financiación.
        with connection_factory() as conn:
            return VentaDAO.obtener_por_id(conn, id_venta)

    def listar_por_cliente(self, id_cliente: int) -> List[VentaVO]:
        # Lazy loading: moto eager, financiación/empleado lazy.
        with connection_factory() as conn:
            return VentaDAO.listar_por_cliente(conn, id_cliente)

    def listar_por_periodo(self, fecha_inicio: str, fecha_fin: str) -> List[VentaVO]:
        # Eager loading: moto y empleado para reportes.
        if fecha_inicio > fecha_fin:
            raise ValueError("La fecha de inicio no puede ser posterior a la de fin.")

        with connection_factory() as conn:
            return VentaDAO.listar_por_periodo(conn, fecha_inicio, fecha_fin)