import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette

from ui.styles import (
    STYLE_GLOBAL, OFF_WHITE, WHITE, TEXT, TEXT2,
    ACCENT, PANEL, BORDER
)
from ui.sidebar import Sidebar
from ui.pages.dashboard   import DashboardPage
from ui.pages.motos       import MotosPage
from ui.pages.clientes    import ClientesPage
from ui.pages.empleados   import EmpleadosPage
from ui.pages.nueva_venta import NuevaVentaPage
from ui.pages.ventas      import VentasPage
from ui.pages.categorias  import CategoriasPage


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self._ctrl = controller
        self.setWindowTitle("MotoXpress — Sistema de Gestión")
        self.setMinimumSize(1120, 720)
        self.resize(1340, 820)
        self.setStyleSheet(STYLE_GLOBAL)
        self._build()

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self._sidebar = Sidebar()
        self._sidebar.page_changed.connect(self._switch_page)
        main_layout.addWidget(self._sidebar)

        # Área de contenido
        self._stack = QStackedWidget()
        self._stack.setStyleSheet(f"background: {OFF_WHITE};")

        # Instanciar páginas
        self._dashboard   = DashboardPage(self._ctrl)
        self._motos       = MotosPage(self._ctrl)
        self._clientes    = ClientesPage(self._ctrl)
        self._empleados   = EmpleadosPage(self._ctrl)
        self._nueva_venta = NuevaVentaPage(self._ctrl)
        self._ventas      = VentasPage(self._ctrl)
        self._categorias  = CategoriasPage(self._ctrl)

        pages = [
            self._dashboard,
            self._motos,
            self._clientes,
            self._empleados,
            self._nueva_venta,
            self._ventas,
            self._categorias,
        ]
        for p in pages:
            self._stack.addWidget(p)

        # Al registrar una venta → refrescar dashboard y ventas
        self._nueva_venta.venta_registrada.connect(self._on_venta_registrada)

        main_layout.addWidget(self._stack)

    def _switch_page(self, idx):
        self._stack.setCurrentIndex(idx)
        # Refresh opcional al entrar a ciertas páginas
        page = self._stack.currentWidget()
        if hasattr(page, 'refresh'):
            page.refresh()

    def _on_venta_registrada(self):
        """Refresca dashboard y ventas después de registrar una venta."""
        # Recrear dashboard para actualizar contadores
        self._stack.removeWidget(self._dashboard)
        self._dashboard.deleteLater()
        self._dashboard = DashboardPage(self._ctrl)
        self._stack.insertWidget(0, self._dashboard)

        # Recargar ventas
        self._ventas.refresh()


def launch_ui(controller):
    app = QApplication(sys.argv)
    app.setApplicationName("MotoXpress")
    app.setStyle("Fusion")

    # Paleta base clara
    palette = QPalette()
    palette.setColor(QPalette.Window,          QColor("#F8F9FB"))
    palette.setColor(QPalette.WindowText,      QColor("#1A1D27"))
    palette.setColor(QPalette.Base,            QColor("#FFFFFF"))
    palette.setColor(QPalette.AlternateBase,   QColor("#F1F3F7"))
    palette.setColor(QPalette.Text,            QColor("#1A1D27"))
    palette.setColor(QPalette.Button,          QColor("#F1F3F7"))
    palette.setColor(QPalette.ButtonText,      QColor("#1A1D27"))
    palette.setColor(QPalette.Highlight,       QColor("#2563EB"))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    palette.setColor(QPalette.Midlight,        QColor("#DDE1E9"))
    app.setPalette(palette)

    window = MainWindow(controller)
    window.show()
    sys.exit(app.exec_())
