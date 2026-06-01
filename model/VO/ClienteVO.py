from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class ClienteVO:
    id_cliente: int
    nombre: str  = field(default=None)
    apellido: str  = field(default=None)
    cedula: str  = field(default=None)
    telefono: str  = field(default=None)
    email:  str  = field(default=None)
    fecha_registro:  datetime  = field(default=None)  
