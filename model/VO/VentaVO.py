from dataclasses import dataclass, field
from typing import Optional, Callable  # Callable se mantiene para los lazy loaders de cliente/moto/empleado
from datetime import datetime

from model.VO.ClienteVO import ClienteVO
from model.VO.MotoVO import MotoVO
from model.VO.EmpleadoVO import EmpleadoVO
from model.VO.FinanciacionVO import FinanciacionVO


@dataclass
class VentaVO:
    id_venta: int
    precio_final: float = field(default=None)
    tipo_pago: str = field(default=None)
    fecha_venta: datetime = field(default=None)
    id_cliente: int = field(default=None)
    id_moto: int = field(default=None)
    id_empleado: int = field(default=None)

    # relacion de composición
    financiacion: Optional[FinanciacionVO] = field(default=None)

    # Lazy loader
    _cliente_loader: Optional[Callable[[], Optional[ClienteVO]]] = field(default=None, repr=False)
    _cliente_cache: Optional[ClienteVO] = field(default=None, repr=False)

    @property
    def cliente(self) -> Optional[ClienteVO]:
        if self._cliente_cache is None and self._cliente_loader:
            self._cliente_cache = self._cliente_loader()
        return self._cliente_cache

    _moto_loader: Optional[Callable[[], Optional[MotoVO]]] = field(default=None, repr=False)
    _moto_cache: Optional[MotoVO] = field(default=None, repr=False)

    @property
    def moto(self) -> Optional[MotoVO]:
        if self._moto_cache is None and self._moto_loader:
            self._moto_cache = self._moto_loader()
        return self._moto_cache

    _empleado_loader: Optional[Callable[[], Optional[EmpleadoVO]]] = field(default=None, repr=False)
    _empleado_cache: Optional[EmpleadoVO] = field(default=None, repr=False)

    @property
    def empleado(self) -> Optional[EmpleadoVO]:
        if self._empleado_cache is None and self._empleado_loader:
            self._empleado_cache = self._empleado_loader()
        return self._empleado_cache

    @property
    def es_financiada(self) -> bool:
        return self.financiacion is not None