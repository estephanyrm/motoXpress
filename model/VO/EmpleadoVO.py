from dataclasses import dataclass, field

@dataclass
class EmpleadoVO:
    id_empleado: int
    nombre: str = field(default=None)
    apellido: str = field(default=None)
    rol: str = field(default=None)
    email:  str = field(default=None)
