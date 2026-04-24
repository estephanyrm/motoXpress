from typing import Optional
from dataclasses import dataclass, field

@dataclass
class CategoriaVO:
    id_categoria = int
    nombre = str
    descripcion = str