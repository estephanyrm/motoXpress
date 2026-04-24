from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class FinanciacionVO:
    id_financiacion: Optional[int]
    cuotas: int = field(default=None)
    interes: float = field(default=None)   
    monto_cuota: float = field(default=None)   
    id_venta: int = field(default=None)

    def generar_plan_cuotas(self) -> List[dict]:
        if self.monto_cuota is None or self.cuotas is None:
            return []

        return [
            {"numero_cuota": i + 1, "monto": self.monto_cuota}
            for i in range(self.cuotas)
        ]

    @property
    def total_a_pagar(self) -> Optional[float]:
        if self.monto_cuota is not None and self.cuotas is not None:
            return round(self.monto_cuota * self.cuotas, 2)
        return None
