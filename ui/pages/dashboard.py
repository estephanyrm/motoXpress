# ─────────────────────────────────────────────
#  MotoXpress — Dashboard
# ─────────────────────────────────────────────
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from ui.styles import (
    STYLE_TABLE, ACCENT, SUCCESS, WARNING, TEXT2, TEXT3,
    DANGER, WHITE, BORDER, PANEL, OFF_WHITE
)
from ui.widgets import make_label, make_divider, StatCard, make_badge, make_status_badge


class DashboardPage(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self._ctrl = controller
        self._build()

    def _build(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        scroll.setWidget(container)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(24)

        # Header
        layout.addWidget(make_label("Dashboard", size=20, bold=True))
        layout.addWidget(make_label("Resumen del sistema MotoXpress", size=13, color=TEXT2))
        layout.addSpacing(4)

        # Stat cards
        try:
            motos     = self._ctrl.motos_disponibles()
            clientes  = self._ctrl.listar_clientes()
            empleados = self._ctrl.listar_empleados()
            cats      = self._ctrl.listar_categorias()
        except Exception:
            motos, clientes, empleados, cats = [], [], [], []

        cards_row = QHBoxLayout()
        cards_row.setSpacing(14)
        cards_data = [
            ("🏍", "Motos disponibles",  str(len(motos)),     ACCENT),
            ("👥", "Clientes",           str(len(clientes)),  SUCCESS),
            ("💼", "Empleados",          str(len(empleados)), WARNING),
            ("🏷", "Categorías",         str(len(cats)),      "#8B5CF6"),
        ]
        for icon, label, val, color in cards_data:
            cards_row.addWidget(StatCard(icon, label, val, color))
        layout.addLayout(cards_row)

        # Tabla de motos recientes
        layout.addSpacing(8)
        layout.addWidget(make_label("Últimas motos disponibles", size=14, bold=True))
        layout.addWidget(make_label("Muestra hasta 10 motos con su categoría", size=12, color=TEXT2))
        layout.addSpacing(4)
        layout.addWidget(self._make_motos_table(motos[:10]))

        layout.addStretch()

    def _make_motos_table(self, motos):
        cols = ["ID", "Marca", "Modelo", "Año", "Color", "Precio", "Categorías", "Estado"]
        tbl = QTableWidget(len(motos), len(cols))
        tbl.setStyleSheet(STYLE_TABLE)
        tbl.setHorizontalHeaderLabels(cols)
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setSelectionBehavior(QTableWidget.SelectRows)
        tbl.verticalHeader().setVisible(False)
        tbl.setFocusPolicy(Qt.NoFocus)
        tbl.setMinimumHeight(260)

        for i, m in enumerate(motos):
            tbl.setItem(i, 0, QTableWidgetItem(str(m.id_moto)))
            tbl.setItem(i, 1, QTableWidgetItem(m.marca or ""))
            tbl.setItem(i, 2, QTableWidgetItem(m.modelo or ""))
            tbl.setItem(i, 3, QTableWidgetItem(str(m.anio or "")))
            tbl.setItem(i, 4, QTableWidgetItem(m.color or ""))

            precio_item = QTableWidgetItem(
                f"${m.precio:,.0f}" if m.precio is not None else "—"
            )
            precio_item.setForeground(QColor(SUCCESS))
            tbl.setItem(i, 5, precio_item)

            # Categorías: cargar lazy si es necesario
            try:
                m.cargar_categorias()
            except Exception:
                pass
            cats_txt = ", ".join(c.nombre for c in m.categorias) if m.categorias else "Sin categoría"
            cat_item = QTableWidgetItem(cats_txt)
            cat_item.setForeground(QColor(TEXT2))
            tbl.setItem(i, 6, cat_item)

            estado_item = QTableWidgetItem(m.estado or "")
            color_map = {"disponible": SUCCESS, "vendida": DANGER, "reservada": WARNING}
            estado_item.setForeground(QColor(color_map.get(m.estado or "", TEXT2)))
            tbl.setItem(i, 7, estado_item)

        return tbl

    def refresh(self):
        """Reconstruye el dashboard."""
        layout = self.layout()
        # Obtener el scroll area y reconectar
        # Más simple: recrear toda la página
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._build()
