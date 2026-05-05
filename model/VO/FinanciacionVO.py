from dataclasses import dataclass, field
from typing import Optional

@dataclass
class FinanciacionVO:
    id_financiacion: Optional[int]
    cuotas: int = field(default=None)
    interes: float = field(default=None)
    monto_cuota: float = field(default=None)
    id_venta: int = field(default=None)