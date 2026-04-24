from dataclasses import dataclass, field
from typing import Optional, List, Callable

from model.VO.CategoriaVO import CategoriaVO


@dataclass
class MotoVO:
    id_moto:  Optional[int]
    vin:      str   = field(default=None)
    marca:    str   = field(default=None)
    modelo:   str   = field(default=None)
    anio:     int   = field(default=None)
    precio:   float = field(default=None)
    color:    str   = field(default=None)
    estado:   str   = field(default='disponible') 

    # Lazy loading de categorías
    _categorias_loader: Optional[Callable[[], List[CategoriaVO]]] = field(
        default=None, repr=False
    )
    _categorias_cache: Optional[List[CategoriaVO]] = field(
        default=None, repr=False
    )

    @property
    def categorias(self) -> Optional[List[CategoriaVO]]:
        if self._categorias_cache is None and self._categorias_loader is not None:
            self._categorias_cache = self._categorias_loader()

        return self._categorias_cache

    @property
    def categorias_cargadas(self) -> bool:
        return self._categorias_cache is not None
