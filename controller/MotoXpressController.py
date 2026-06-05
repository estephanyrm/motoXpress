from typing import List, Optional

from postgres.model.VO.VentaVO import VentaVO
from postgres.model.VO.FinanciacionVO import FinanciacionVO
from postgres.model.VO.ClienteVO import ClienteVO
from mongo.model.VO.MotoVO import MotoVO

from service.VentaService import VentaService
from service.MotoService import MotoService
from service.ClienteService import ClienteService
from service.EmpleadoService import EmpleadoService
from service.CategoriaService import CategoriaService


class MotoXpressController:

    def __init__(self,
                 venta_service: VentaService,
                 moto_service: MotoService,
                 cliente_service: ClienteService,
                 empleado_service: EmpleadoService,
                 categoria_service: CategoriaService):
        self._ventas     = venta_service
        self._motos      = moto_service
        self._clientes   = cliente_service
        self._empleados  = empleado_service
        self._categorias = categoria_service

    # Ventas
    def registrar_venta(self, venta: VentaVO, financiacion: Optional[FinanciacionVO] = None) -> int:
        return self._ventas.registrar(venta, financiacion)

    def deshacer_venta(self) -> bool:
        return self._ventas.deshacer_ultima_venta()

    def rehacer_venta(self) -> bool:
        return self._ventas.rehacer_ultima_venta()

    def puede_deshacer_venta(self) -> bool:
        return self._ventas.puede_deshacer()

    def puede_rehacer_venta(self) -> bool:
        return self._ventas.puede_rehacer()

    def ventas_por_cliente(self, id_cliente: int) -> List[VentaVO]:
        return self._ventas.listar_por_cliente(id_cliente)

    def ventas_por_periodo(self, fecha_inicio: str, fecha_fin: str) -> List[VentaVO]:
        return self._ventas.listar_por_periodo(fecha_inicio, fecha_fin)

    # Motos
    def motos_disponibles(self) -> List[MotoVO]:
        return self._motos.listar_disponibles()

    def detalle_moto(self, id_moto: int) -> Optional[MotoVO]:
        return self._motos.obtener_detalle(id_moto)

    def registrar_moto(self, moto: MotoVO, ids_categorias: Optional[List[int]] = None) -> int:
        return self._motos.registrar(moto, ids_categorias)

    # Clientes
    def listar_clientes(self) -> List[ClienteVO]:
        return self._clientes.listar()

    def registrar_cliente(self, cliente: ClienteVO) -> int:
        return self._clientes.registrar(cliente)

    # Empleados
    def listar_empleados(self):
        return self._empleados.listar()

    # Categorías
    def listar_categorias(self):
        return self._categorias.listar_todas()

    def crear_categoria(self, nombre: str, descripcion: str = None) -> int:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        return self._categorias.crear(nombre.strip(), descripcion)

    def actualizar_categoria(self, id_categoria: int, nombre: str, descripcion: str = None) -> None:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        self._categorias.actualizar(id_categoria, nombre.strip(), descripcion)

    def eliminar_categoria(self, id_categoria: int) -> None:
        self._categorias.eliminar(id_categoria)
