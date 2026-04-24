from dataclasses import dataclass, field
from typing import Optional, Callable
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

    # Lazy de la financiacion
    _financiacion_loader: Optional[Callable[[], Optional[FinanciacionVO]]] = field(
        default=None, repr=False
    )
    _financiacion_cache: Optional[FinanciacionVO] = field(
        default=None, repr=False
    )

    @property
    def financiacion(self) -> Optional[FinanciacionVO]:
        if self._financiacion_cache is None and self._financiacion_loader is not None:
            self._financiacion_cache = self._financiacion_loader()
        return self._financiacion_cache

    # Lazy del cliente 
    _cliente_loader: Optional[Callable[[], Optional[ClienteVO]]] = field(
        default=None, repr=False
    )
    _cliente_cache: Optional[ClienteVO] = field(
        default=None, repr=False
    )

    @property
    def cliente(self) -> Optional[ClienteVO]:
        if self._cliente_cache is None and self._cliente_loader is not None:
            self._cliente_cache = self._cliente_loader()
        return self._cliente_cache

    # Lazy de la moto 
    _moto_loader: Optional[Callable[[], Optional[MotoVO]]] = field(
        default=None, repr=False
    )
    _moto_cache: Optional[MotoVO] = field(
        default=None, repr=False
    )

    @property
    def moto(self) -> Optional[MotoVO]:
        if self._moto_cache is None and self._moto_loader is not None:
            self._moto_cache = self._moto_loader()
        return self._moto_cache

    # Lazy del empleado
    _empleado_loader: Optional[Callable[[], Optional[EmpleadoVO]]] = field(
        default=None, repr=False
    )
    _empleado_cache: Optional[EmpleadoVO] = field(
        default=None, repr=False
    )

    @property
    def empleado(self) -> Optional[EmpleadoVO]:
        if self._empleado_cache is None and self._empleado_loader is not None:
            self._empleado_cache = self._empleado_loader()
        return self._empleado_cache

    @property
    def es_financiada(self) -> bool:
        return self.tipo_pago == 'financiado'

    @property
    def financiacion_cargada(self) -> bool:
        return self._financiacion_cache is not None
