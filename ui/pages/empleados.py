# ─────────────────────────────────────────────
#  MotoXpress — Página de Empleados
# ─────────────────────────────────────────────
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton,
    QLineEdit, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from ui.styles import (
    STYLE_TABLE, STYLE_INPUT,
    ACCENT, SUCCESS, WARNING, DANGER, TEXT, TEXT2, TEXT3,
    WHITE, btn_secondary
)
from ui.widgets import make_label, show_error


class EmpleadosPage(QWidget):
    ROL_COLORS = {
        "vendedor":       ACCENT,
        "administrador":  WARNING,
        "mecanico":       SUCCESS,
    }

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self._ctrl = controller
        self._all_empleados = []
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        # ── Encabezado ──
        header = QHBoxLayout()
        header.setSpacing(12)
        hv = QVBoxLayout()
        hv.setSpacing(4)
        hv.addWidget(make_label("Empleados", size=20, bold=True))
        hv.addWidget(make_label("Personal registrado en el sistema", size=13, color=TEXT2))
        header.addLayout(hv)
        header.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("Buscar por nombre…")
        self._search.setFixedWidth(220)
        self._search.setStyleSheet(STYLE_INPUT)
        self._search.textChanged.connect(self._apply_filters)
        header.addWidget(self._search)

        self._combo_rol = QComboBox()
        self._combo_rol.addItems(["Todos los roles", "vendedor", "administrador", "mecanico"])
        self._combo_rol.setFixedWidth(180)
        self._combo_rol.setStyleSheet(STYLE_INPUT)
        self._combo_rol.currentIndexChanged.connect(self._apply_filters)
        header.addWidget(self._combo_rol)

        layout.addLayout(header)

        # ── Tabla ──
        cols = ["ID", "Nombre", "Apellido", "Rol", "Email"]
        self._tbl = QTableWidget(0, len(cols))
        self._tbl.setStyleSheet(STYLE_TABLE)
        self._tbl.setHorizontalHeaderLabels(cols)
        hh = self._tbl.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.Stretch)
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        self._tbl.setFocusPolicy(Qt.NoFocus)
        self._tbl.setAlternatingRowColors(True)
        layout.addWidget(self._tbl)

        self._reload()

    def _reload(self):
        try:
            self._all_empleados = self._ctrl.listar_empleados()
        except Exception as e:
            show_error(self, str(e))
            self._all_empleados = []
        self._apply_filters()

    def _apply_filters(self):
        text = self._search.text().lower().strip()
        rol  = self._combo_rol.currentText()
        result = self._all_empleados

        if text:
            result = [
                e for e in result
                if text in (e.nombre or "").lower()
                or text in (e.apellido or "").lower()
                or text in (e.email or "").lower()
            ]

        if rol != "Todos los roles":
            rol = rol.lower().strip()
            result = [
                e for e in result
                if (e.rol or "").lower().strip() == rol
            ]

        self._populate(result)

    def _populate(self, empleados):
        self._tbl.setRowCount(len(empleados))
        for i, e in enumerate(empleados):
            self._tbl.setItem(i, 0, QTableWidgetItem(str(e.id_empleado)))
            self._tbl.setItem(i, 1, QTableWidgetItem(e.nombre or ""))
            self._tbl.setItem(i, 2, QTableWidgetItem(e.apellido or ""))

            rol_item = QTableWidgetItem((e.rol or "").capitalize())
            color = self.ROL_COLORS.get(e.rol or "", TEXT2)
            rol_item.setForeground(QColor(color))
            self._tbl.setItem(i, 3, rol_item)

            self._tbl.setItem(i, 4, QTableWidgetItem(e.email or "—"))

        self._tbl.resizeRowsToContents()
