from typing import List, Optional

from db.gestor_conexiones import connection_factory
from model.DAO.VentaDAO import VentaDAO
from model.DAO.MotoDAO import MotoDAO
from model.DAO.ClienteDAO import ClienteDAO
from model.DAO.EmpleadoDAO import EmpleadoDAO
from model.DAO.FinanciacionDAO import FinanciacionDAO
from model.VO.VentaVO import VentaVO
from model.VO.FinanciacionVO import FinanciacionVO

_TIPOS_PAGO = {'contado', 'financiado', 'tarjeta'}


class VentaService:

    def registrar(self,
                  venta: VentaVO,
                  financiacion: Optional[FinanciacionVO] = None) -> int:
        """
        Registra una venta en una sola transacción atómica:
          1. Valida que el cliente, la moto y el empleado existan.
          2. Valida que la moto esté disponible.
          3. Inserta la Venta.
          4. Cambia el estado de la moto a 'vendida'.
          5. Si tipo_pago == 'financiado', calcula monto_cuota e inserta Financiacion.

        Retorna el id_venta generado.
        """
        if venta.tipo_pago not in _TIPOS_PAGO:
            raise ValueError(
                f"Tipo de pago '{venta.tipo_pago}' no válido. "
                f"Valores permitidos: {_TIPOS_PAGO}"
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

        with connection_factory() as conexion:

            # --- Validaciones de existencia ---
            cliente = ClienteDAO.obtener_por_id(conexion, venta.id_cliente)
            if cliente is None:
                raise ValueError(f"No existe cliente con id {venta.id_cliente}.")

            moto = MotoDAO.obtener_por_id(conexion, venta.id_moto)
            if moto is None:
                raise ValueError(f"No existe moto con id {venta.id_moto}.")
            if moto.estado != 'disponible':
                raise ValueError(
                    f"La moto '{moto.marca} {moto.modelo}' no está disponible "
                    f"(estado actual: '{moto.estado}')."
                )

            empleado = EmpleadoDAO.obtener_por_id(conexion, venta.id_empleado)
            if empleado is None:
                raise ValueError(f"No existe empleado con id {venta.id_empleado}.")

            # --- 1. Insertar venta ---
            id_venta = VentaDAO.insertar(conexion, venta)

            # --- 2. Marcar moto como vendida ---
            MotoDAO.actualizar_estado(conexion, venta.id_moto, 'vendida')

            # --- 3. Insertar financiación si aplica ---
            if venta.tipo_pago == 'financiado':
                financiacion.id_venta = id_venta
                # Regla de negocio: monto_cuota = precio * (1 + interes%) / cuotas
                financiacion.monto_cuota = round(
                    venta.precio_final * (1 + financiacion.interes / 100) / financiacion.cuotas,
                    2
                )
                FinanciacionDAO.insertar(conexion, financiacion)

            return id_venta

    def obtener_detalle(self, id_venta: int) -> Optional[VentaVO]:
        """Eager loading: retorna la venta con cliente, moto, empleado y financiación."""
        with connection_factory() as conexion:
            return VentaDAO.obtener_por_id(conexion, id_venta)

    def listar_por_cliente(self, id_cliente: int) -> List[VentaVO]:
        """Lazy loading: retorna ventas con moto eager y financiación/empleado lazy."""
        with connection_factory() as conexion:
            return VentaDAO.listar_por_cliente(conexion, id_cliente)

    def listar_por_periodo(self, fecha_inicio: str, fecha_fin: str) -> List[VentaVO]:
        """
        Eager loading: retorna ventas con moto y empleado para reportes.
        Fechas en formato 'YYYY-MM-DD'.
        """
        if fecha_inicio > fecha_fin:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        with connection_factory() as conexion:
            return VentaDAO.listar_por_periodo(conexion, fecha_inicio, fecha_fin)
