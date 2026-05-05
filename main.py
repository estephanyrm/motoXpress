import sys
import os

# Permite ejecutar desde cualquier directorio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model.COMMAND.UndoRedoManager import UndoRedoManager

from service.VentaService    import VentaService
from service.MotoService     import MotoService
from service.ClienteService  import ClienteService
from service.EmpleadoService import EmpleadoService
from service.CategoriaService import CategoriaService

from controller.MotoXpressController import MotoXpressController
from ui.pyqt5_view import launch_ui


def build_controller() -> MotoXpressController:
    undo_redo = UndoRedoManager()

    venta_service     = VentaService(undo_redo)
    moto_service      = MotoService()
    cliente_service   = ClienteService()
    empleado_service  = EmpleadoService()
    categoria_service = CategoriaService()

    return MotoXpressController(
        venta_service=venta_service,
        moto_service=moto_service,
        cliente_service=cliente_service,
        empleado_service=empleado_service,
        categoria_service=categoria_service,
    )


def main():
    controller = build_controller()
    launch_ui(controller) 


if __name__ == "__main__":
    main()
