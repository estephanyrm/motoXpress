from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CategoriaVO:
    id_categoria: int
    nombre: str = field(default=None)
    descripcion: Optional[str] = field(default=None)