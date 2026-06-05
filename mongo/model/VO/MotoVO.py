from dataclasses import dataclass, field
from typing import Optional, List

from mongo.model.VO.CategoriaVO import CategoriaVO


@dataclass
class MotoVO:
    id_moto: int
    vin: str = field(default=None)
    marca: str = field(default=None)
    modelo: str = field(default=None)
    anio: int = field(default=None)
    precio: float = field(default=None)
    color: str = field(default=None)
    estado: str = field(default='disponible')

    # relacion de agregacion
    categorias: List[CategoriaVO] = field(default_factory=list)

    @property
    def esta_disponible(self) -> bool:
        return self.estado == 'disponible'
