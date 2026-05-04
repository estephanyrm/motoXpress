import sys
from typing import Optional, List

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QSpinBox,
    QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QFrame, QScrollArea, QMessageBox, QHeaderView,
    QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QLinearGradient, QBrush,
    QPainter, QPen, QPixmap, QIcon, QFontDatabase
)

# ── Paleta de colores ────────────────────────────────────────────────────────
BG          = "#0F1117"
BG2         = "#161B27"
BG3         = "#1E2538"
CARD        = "#1A2035"
ACCENT      = "#4F6EF7"
ACCENT2     = "#7C3AED"
SUCCESS     = "#22C55E"
DANGER      = "#EF4444"
WARNING     = "#F59E0B"
TEXT        = "#E8EAF6"
TEXT2       = "#8892B0"
BORDER      = "#2A3352"
HIGHLIGHT   = "#2D3A6B"

STYLE_GLOBAL = f"""
QWidget {{
    background-color: {BG};
    color: {TEXT};
    font-family: 'Segoe UI', 'Ubuntu', 'DejaVu Sans', sans-serif;
    font-size: 13px;
}}
QScrollBar:vertical {{
    background: {BG2};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 4px;
    min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""

def card_style(extra=""):
    return f"""
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-radius: 12px;
        {extra}
    """

def btn_primary(extra=""):
    return f"""
        QPushButton {{
            background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {ACCENT}, stop:1 {ACCENT2});
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            font-size: 13px;
            {extra}
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 #6080FF, stop:1 #9040FF);
        }}
        QPushButton:pressed {{
            background: {ACCENT};
        }}
        QPushButton:disabled {{
            background: {BORDER};
            color: {TEXT2};
        }}
    """

def btn_secondary():
    return f"""
        QPushButton {{
            background: {BG3};
            color: {TEXT};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 8px 18px;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background: {HIGHLIGHT};
            border-color: {ACCENT};
        }}
    """

def btn_danger():
    return f"""
        QPushButton {{
            background: transparent;
            color: {DANGER};
            border: 1px solid {DANGER};
            border-radius: 8px;
            padding: 8px 18px;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background: rgba(239,68,68,0.12);
        }}
    """

def input_style():
    return f"""
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
            background: {BG2};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 8px 12px;
            color: {TEXT};
            font-size: 13px;
        }}
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {ACCENT};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 24px;
        }}
        QComboBox QAbstractItemView {{
            background: {BG2};
            border: 1px solid {BORDER};
            selection-background-color: {HIGHLIGHT};
            color: {TEXT};
        }}
    """

def table_style():
    return f"""
        QTableWidget {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 8px;
            gridline-color: {BORDER};
            color: {TEXT};
            font-size: 12px;
        }}
        QHeaderView::section {{
            background: {BG3};
            color: {TEXT2};
            border: none;
            border-bottom: 1px solid {BORDER};
            padding: 8px 12px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        QTableWidget::item {{
            padding: 8px 12px;
            border-bottom: 1px solid {BORDER};
        }}
        QTableWidget::item:selected {{
            background: {HIGHLIGHT};
            color: {TEXT};
        }}
    """


# ── Helpers de UI ────────────────────────────────────────────────────────────

def make_label(text, size=13, bold=False, color=TEXT, wrap=False):
    lbl = QLabel(text)
    lbl.setStyleSheet(f"color: {color}; font-size: {size}px; "
                      f"font-weight: {'600' if bold else '400'}; background: transparent;")
    if wrap:
        lbl.setWordWrap(True)
    return lbl

def make_badge(text, color=ACCENT):
    b = QLabel(text)
    b.setStyleSheet(f"""
        background: rgba(79,110,247,0.15);
        color: {color};
        border: 1px solid {color};
        border-radius: 10px;
        padding: 2px 10px;
        font-size: 11px;
        font-weight: 600;
    """)
    b.setAlignment(Qt.AlignCenter)
    return b

def make_divider():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet(f"color: {BORDER}; background: {BORDER};")
    line.setFixedHeight(1)
    return line

def show_error(parent, msg):
    d = QMessageBox(parent)
    d.setWindowTitle("Error")
    d.setText(msg)
    d.setIcon(QMessageBox.Warning)
    d.setStyleSheet(f"background:{BG2}; color:{TEXT}; border:1px solid {BORDER};")
    d.exec_()

def show_ok(parent, msg):
    d = QMessageBox(parent)
    d.setWindowTitle("Listo")
    d.setText(msg)
    d.setIcon(QMessageBox.Information)
    d.setStyleSheet(f"background:{BG2}; color:{TEXT};")
    d.exec_()


# ── Sidebar ──────────────────────────────────────────────────────────────────

class Sidebar(QWidget):
    page_changed = pyqtSignal(int)

    ITEMS = [
        ("🏠", "Dashboard"),
        ("🏍", "Motos"),
        ("👥", "Clientes"),
        ("💼", "Empleados"),
        ("🧾", "Nueva Venta"),
        ("📊", "Ventas"),
        ("🏷", "Categorías"),
    ]

    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)
        self.setStyleSheet(f"background: {BG2}; border-right: 1px solid {BORDER};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo
        logo_wrap = QWidget()
        logo_wrap.setFixedHeight(72)
        logo_wrap.setStyleSheet(f"background: {BG2}; border-bottom: 1px solid {BORDER};")
        ll = QHBoxLayout(logo_wrap)
        ll.setContentsMargins(20, 0, 20, 0)
        icon = make_label("🏍", size=24)
        title = make_label("MotoXpress", size=16, bold=True)
        ll.addWidget(icon)
        ll.addWidget(title)
        ll.addStretch()
        layout.addWidget(logo_wrap)

        layout.addSpacing(12)

        self._buttons = []
        for i, (emoji, label) in enumerate(self.ITEMS):
            btn = QPushButton(f"  {emoji}  {label}")
            btn.setCheckable(True)
            btn.setFixedHeight(44)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(self._btn_style(False))
            btn.clicked.connect(lambda _, idx=i: self._select(idx))
            layout.addWidget(btn)
            self._buttons.append(btn)

        layout.addStretch()

        ver = make_label("v1.0.0", size=11, color=TEXT2)
        ver.setContentsMargins(20, 0, 0, 16)
        layout.addWidget(ver)

        self._select(0)

    def _btn_style(self, active):
        if active:
            return f"""
                QPushButton {{
                    background: {HIGHLIGHT};
                    color: {TEXT};
                    border: none;
                    border-left: 3px solid {ACCENT};
                    text-align: left;
                    padding: 0 16px;
                    font-size: 13px;
                    font-weight: 600;
                }}
            """
        return f"""
            QPushButton {{
                background: transparent;
                color: {TEXT2};
                border: none;
                border-left: 3px solid transparent;
                text-align: left;
                padding: 0 16px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {BG3};
                color: {TEXT};
            }}
        """

    def _select(self, idx):
        for i, b in enumerate(self._buttons):
            b.setChecked(i == idx)
            b.setStyleSheet(self._btn_style(i == idx))
        self.page_changed.emit(idx)


# ── Dashboard ────────────────────────────────────────────────────────────────

class DashboardPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Header
        layout.addWidget(make_label("Dashboard", size=24, bold=True))
        layout.addWidget(make_label("Resumen del concesionario", color=TEXT2))

        # Stat cards
        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)

        try:
            motos = self._ctrl.motos_disponibles()
            clientes = self._ctrl.listar_clientes()
            empleados = self._ctrl.listar_empleados()
            cats = self._ctrl.listar_categorias()
        except Exception:
            motos, clientes, empleados, cats = [], [], [], []

        cards_data = [
            ("🏍", "Motos disponibles", str(len(motos)), ACCENT),
            ("👥", "Clientes", str(len(clientes)), SUCCESS),
            ("💼", "Empleados", str(len(empleados)), WARNING),
            ("🏷", "Categorías", str(len(cats)), ACCENT2),
        ]
        for emoji, label, value, color in cards_data:
            stats_row.addWidget(self._stat_card(emoji, label, value, color))
        layout.addLayout(stats_row)

        # Motos recientes
        layout.addWidget(make_label("Motos disponibles", size=15, bold=True))
        tbl = self._motos_table(motos[:8])
        layout.addWidget(tbl)
        layout.addStretch()

    def _stat_card(self, emoji, label, value, color):
        card = QFrame()
        card.setStyleSheet(card_style())
        vl = QVBoxLayout(card)
        vl.setContentsMargins(20, 20, 20, 20)
        vl.setSpacing(8)
        top = QHBoxLayout()
        top.addWidget(make_label(emoji, size=20))
        top.addStretch()
        vl.addLayout(top)
        vl.addWidget(make_label(value, size=28, bold=True, color=color))
        vl.addWidget(make_label(label, size=12, color=TEXT2))
        return card

    def _motos_table(self, motos):
        tbl = QTableWidget(len(motos), 6)
        tbl.setStyleSheet(table_style())
        tbl.setHorizontalHeaderLabels(["ID", "Marca", "Modelo", "Año", "Precio", "Estado"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setSelectionBehavior(QTableWidget.SelectRows)
        tbl.verticalHeader().setVisible(False)
        for i, m in enumerate(motos):
            tbl.setItem(i, 0, QTableWidgetItem(str(m.id_moto)))
            tbl.setItem(i, 1, QTableWidgetItem(m.marca or ""))
            tbl.setItem(i, 2, QTableWidgetItem(m.modelo or ""))
            tbl.setItem(i, 3, QTableWidgetItem(str(m.anio or "")))
            precio_item = QTableWidgetItem(f"${m.precio:,.0f}" if m.precio else "")
            precio_item.setForeground(QColor(SUCCESS))
            tbl.setItem(i, 4, precio_item)
            estado_item = QTableWidgetItem(m.estado or "")
            estado_item.setForeground(QColor(SUCCESS if m.estado == 'disponible' else DANGER))
            tbl.setItem(i, 5, estado_item)
        return tbl


# ── Motos ────────────────────────────────────────────────────────────────────

class MotosPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # Header + filtro
        header = QHBoxLayout()
        header.addWidget(make_label("Motos disponibles", size=22, bold=True))
        header.addStretch()
        self._search = QLineEdit()
        self._search.setPlaceholderText("Buscar por marca o modelo…")
        self._search.setFixedWidth(260)
        self._search.setStyleSheet(input_style())
        self._search.textChanged.connect(self._filter)
        header.addWidget(self._search)

        btn_reg = QPushButton("+ Registrar moto")
        btn_reg.setStyleSheet(btn_primary())
        btn_reg.setCursor(Qt.PointingHandCursor)
        btn_reg.clicked.connect(self._form_registrar)
        header.addWidget(btn_reg)
        layout.addLayout(header)

        # Tabla
        self._tbl = QTableWidget(0, 7)
        self._tbl.setStyleSheet(table_style())
        self._tbl.setHorizontalHeaderLabels(
            ["ID", "VIN", "Marca", "Modelo", "Año", "Precio", "Estado"])
        self._tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        layout.addWidget(self._tbl)

        self._all_motos = []
        self._reload()

    def _reload(self):
        try:
            self._all_motos = self._ctrl.motos_disponibles()
        except Exception as e:
            show_error(self, str(e))
            self._all_motos = []
        self._populate(self._all_motos)

    def _filter(self, text):
        t = text.lower()
        filtered = [m for m in self._all_motos
                    if t in (m.marca or "").lower() or t in (m.modelo or "").lower()]
        self._populate(filtered)

    def _populate(self, motos):
        self._tbl.setRowCount(len(motos))
        for i, m in enumerate(motos):
            self._tbl.setItem(i, 0, QTableWidgetItem(str(m.id_moto)))
            self._tbl.setItem(i, 1, QTableWidgetItem(m.vin or ""))
            self._tbl.setItem(i, 2, QTableWidgetItem(m.marca or ""))
            self._tbl.setItem(i, 3, QTableWidgetItem(m.modelo or ""))
            self._tbl.setItem(i, 4, QTableWidgetItem(str(m.anio or "")))
            p = QTableWidgetItem(f"${m.precio:,.0f}" if m.precio else "")
            p.setForeground(QColor(SUCCESS))
            self._tbl.setItem(i, 4, QTableWidgetItem(str(m.anio or "")))
            self._tbl.setItem(i, 5, p)
            e = QTableWidgetItem(m.estado or "")
            e.setForeground(QColor(SUCCESS if m.estado == 'disponible' else WARNING))
            self._tbl.setItem(i, 6, e)

    def _form_registrar(self):
        dialog = _MotoDialog(self, self._ctrl)
        if dialog.exec_():
            self._reload()


class _MotoDialog(QMessageBox):
    """Usa un QDialog simple embebido en un formulario."""
    pass


# Usamos un QWidget como diálogo manual
class _MotoDialog(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent, Qt.Dialog | Qt.WindowCloseButtonHint)
        self._ctrl = controller
        self.setWindowTitle("Registrar nueva moto")
        self.setFixedSize(460, 480)
        self.setStyleSheet(f"background: {BG2};")
        self._result = False
        self._build()
        self.show()

    def exec_(self):
        # Simulamos modal con show(); para simplicidad retornamos _result
        return False

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(14)
        layout.addWidget(make_label("Nueva moto", size=18, bold=True))
        layout.addWidget(make_divider())

        form = QFormLayout()
        form.setSpacing(10)

        self._vin   = QLineEdit(); self._vin.setStyleSheet(input_style())
        self._marca = QLineEdit(); self._marca.setStyleSheet(input_style())
        self._model = QLineEdit(); self._model.setStyleSheet(input_style())
        self._anio  = QSpinBox();  self._anio.setRange(1990, 2030); self._anio.setValue(2024)
        self._anio.setStyleSheet(input_style())
        self._precio = QDoubleSpinBox(); self._precio.setRange(0, 99999999)
        self._precio.setPrefix("$"); self._precio.setStyleSheet(input_style())
        self._color = QLineEdit(); self._color.setStyleSheet(input_style())

        for lbl, w in [("VIN", self._vin), ("Marca", self._marca),
                        ("Modelo", self._model), ("Año", self._anio),
                        ("Precio", self._precio), ("Color", self._color)]:
            lbl_w = make_label(lbl, color=TEXT2, size=12)
            form.addRow(lbl_w, w)
        layout.addLayout(form)

        layout.addStretch()
        btn = QPushButton("Registrar")
        btn.setStyleSheet(btn_primary())
        btn.clicked.connect(self._save)
        layout.addWidget(btn)

    def _save(self):
        from model.VO.MotoVO import MotoVO
        try:
            moto = MotoVO(
                id_moto=0,
                vin=self._vin.text().strip(),
                marca=self._marca.text().strip(),
                modelo=self._model.text().strip(),
                anio=self._anio.value(),
                precio=self._precio.value(),
                color=self._color.text().strip(),
                estado='disponible',
            )
            self._ctrl.registrar_moto(moto)
            show_ok(self, "Moto registrada exitosamente.")
            self.close()
        except Exception as e:
            show_error(self, str(e))


# ── Clientes ─────────────────────────────────────────────────────────────────

class ClientesPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        header = QHBoxLayout()
        header.addWidget(make_label("Clientes", size=22, bold=True))
        header.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("Buscar por cédula…")
        self._search.setFixedWidth(220)
        self._search.setStyleSheet(input_style())
        self._search.returnPressed.connect(self._buscar_cedula)
        header.addWidget(self._search)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.setStyleSheet(btn_secondary())
        btn_buscar.clicked.connect(self._buscar_cedula)
        header.addWidget(btn_buscar)

        btn_reg = QPushButton("+ Registrar cliente")
        btn_reg.setStyleSheet(btn_primary())
        btn_reg.clicked.connect(self._form_registrar)
        header.addWidget(btn_reg)
        layout.addLayout(header)

        self._tbl = QTableWidget(0, 6)
        self._tbl.setStyleSheet(table_style())
        self._tbl.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Apellido", "Cédula", "Teléfono", "Email"])
        self._tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        layout.addWidget(self._tbl)
        self._reload()

    def _reload(self):
        try:
            clientes = self._ctrl.listar_clientes()
        except Exception as e:
            show_error(self, str(e)); return
        self._populate(clientes)

    def _populate(self, clientes):
        self._tbl.setRowCount(len(clientes))
        for i, c in enumerate(clientes):
            self._tbl.setItem(i, 0, QTableWidgetItem(str(c.id_cliente)))
            self._tbl.setItem(i, 1, QTableWidgetItem(c.nombre or ""))
            self._tbl.setItem(i, 2, QTableWidgetItem(c.apellido or ""))
            self._tbl.setItem(i, 3, QTableWidgetItem(c.cedula or ""))
            self._tbl.setItem(i, 4, QTableWidgetItem(c.telefono or ""))
            self._tbl.setItem(i, 5, QTableWidgetItem(c.email or ""))

    def _buscar_cedula(self):
        cedula = self._search.text().strip()
        if not cedula:
            self._reload(); return
        try:
            c = self._ctrl.buscar_cliente_cedula(cedula)
            if c:
                self._populate([c])
            else:
                show_error(self, f"No se encontró cliente con cédula '{cedula}'.")
        except Exception as e:
            show_error(self, str(e))

    def _form_registrar(self):
        dlg = _ClienteDialog(self, self._ctrl)


class _ClienteDialog(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent, Qt.Dialog | Qt.WindowCloseButtonHint)
        self._ctrl = controller
        self.setWindowTitle("Registrar cliente")
        self.setFixedSize(420, 420)
        self.setStyleSheet(f"background: {BG2};")
        self._build()
        self.show()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(12)
        layout.addWidget(make_label("Nuevo cliente", size=18, bold=True))
        layout.addWidget(make_divider())

        form = QFormLayout(); form.setSpacing(10)
        self._nombre   = QLineEdit(); self._nombre.setStyleSheet(input_style())
        self._apellido = QLineEdit(); self._apellido.setStyleSheet(input_style())
        self._cedula   = QLineEdit(); self._cedula.setStyleSheet(input_style())
        self._telefono = QLineEdit(); self._telefono.setStyleSheet(input_style())
        self._email    = QLineEdit(); self._email.setStyleSheet(input_style())

        for lbl, w in [("Nombre*", self._nombre), ("Apellido*", self._apellido),
                        ("Cédula*", self._cedula), ("Teléfono", self._telefono),
                        ("Email", self._email)]:
            form.addRow(make_label(lbl, color=TEXT2, size=12), w)
        layout.addLayout(form)
        layout.addStretch()

        btn = QPushButton("Registrar")
        btn.setStyleSheet(btn_primary())
        btn.clicked.connect(self._save)
        layout.addWidget(btn)

    def _save(self):
        from model.VO.ClienteVO import ClienteVO
        try:
            c = ClienteVO(
                id_cliente=0,
                nombre=self._nombre.text().strip(),
                apellido=self._apellido.text().strip(),
                cedula=self._cedula.text().strip(),
                telefono=self._telefono.text().strip(),
                email=self._email.text().strip(),
            )
            self._ctrl.registrar_cliente(c)
            show_ok(self, "Cliente registrado.")
            self.close()
        except Exception as e:
            show_error(self, str(e))


# ── Empleados ────────────────────────────────────────────────────────────────

class EmpleadosPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        header = QHBoxLayout()
        header.addWidget(make_label("Empleados", size=22, bold=True))
        header.addStretch()
        combo = QComboBox()
        combo.addItems(["Todos", "vendedor", "administrador", "mecanico"])
        combo.setStyleSheet(input_style())
        combo.setFixedWidth(180)
        combo.currentTextChanged.connect(self._filtrar_rol)
        header.addWidget(combo)
        layout.addLayout(header)

        self._tbl = QTableWidget(0, 5)
        self._tbl.setStyleSheet(table_style())
        self._tbl.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Rol", "Email"])
        self._tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        layout.addWidget(self._tbl)
        self._reload()

    def _reload(self):
        try:
            emps = self._ctrl.listar_empleados()
        except Exception as e:
            show_error(self, str(e)); return
        self._populate(emps)

    def _filtrar_rol(self, rol):
        if rol == "Todos":
            self._reload(); return
        try:
            emps = self._ctrl.listar_empleados_por_rol(rol)
            self._populate(emps)
        except Exception as e:
            show_error(self, str(e))

    def _populate(self, emps):
        rol_colors = {"vendedor": ACCENT, "administrador": WARNING, "mecanico": SUCCESS}
        self._tbl.setRowCount(len(emps))
        for i, e in enumerate(emps):
            self._tbl.setItem(i, 0, QTableWidgetItem(str(e.id_empleado)))
            self._tbl.setItem(i, 1, QTableWidgetItem(e.nombre or ""))
            self._tbl.setItem(i, 2, QTableWidgetItem(e.apellido or ""))
            rol_item = QTableWidgetItem(e.rol or "")
            rol_item.setForeground(QColor(rol_colors.get(e.rol or "", TEXT2)))
            self._tbl.setItem(i, 3, rol_item)
            self._tbl.setItem(i, 4, QTableWidgetItem(e.email or ""))


# ── Nueva Venta ──────────────────────────────────────────────────────────────

class NuevaVentaPage(QWidget):
    venta_registrada = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        scroll.setWidget(container)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        layout.addWidget(make_label("Nueva Venta", size=22, bold=True))
        layout.addWidget(make_label("Completa los datos para registrar la venta",
                                    color=TEXT2))

        # Card principal
        card = QFrame(); card.setStyleSheet(card_style())
        cl = QVBoxLayout(card); cl.setContentsMargins(24, 24, 24, 24); cl.setSpacing(16)

        form = QFormLayout(); form.setSpacing(12)

        # Selección de cliente
        self._id_cliente = QSpinBox()
        self._id_cliente.setRange(1, 99999)
        self._id_cliente.setStyleSheet(input_style())
        form.addRow(make_label("ID Cliente*", color=TEXT2, size=12), self._id_cliente)

        # Selección de moto
        self._moto_combo = QComboBox()
        self._moto_combo.setStyleSheet(input_style())
        self._cargar_motos()
        form.addRow(make_label("Moto*", color=TEXT2, size=12), self._moto_combo)

        # Empleado
        self._id_empleado = QSpinBox()
        self._id_empleado.setRange(1, 99999)
        self._id_empleado.setStyleSheet(input_style())
        form.addRow(make_label("ID Empleado*", color=TEXT2, size=12), self._id_empleado)

        # Precio final
        self._precio = QDoubleSpinBox()
        self._precio.setRange(0, 99999999)
        self._precio.setPrefix("$")
        self._precio.setStyleSheet(input_style())
        form.addRow(make_label("Precio final*", color=TEXT2, size=12), self._precio)

        # Tipo de pago
        self._tipo_pago = QComboBox()
        self._tipo_pago.addItems(["contado", "financiado", "tarjeta"])
        self._tipo_pago.setStyleSheet(input_style())
        self._tipo_pago.currentTextChanged.connect(self._toggle_financiacion)
        form.addRow(make_label("Tipo de pago*", color=TEXT2, size=12), self._tipo_pago)

        cl.addLayout(form)

        # Panel financiación (oculto por defecto)
        self._fin_frame = QFrame()
        self._fin_frame.setStyleSheet(f"""
            background: {BG3};
            border: 1px solid {BORDER};
            border-radius: 8px;
        """)
        fl = QFormLayout(self._fin_frame)
        fl.setContentsMargins(16, 16, 16, 16)
        fl.setSpacing(10)

        fin_title = make_label("Plan de financiación", size=14, bold=True, color=ACCENT)
        fl.addRow(fin_title)

        self._cuotas = QSpinBox(); self._cuotas.setRange(1, 60); self._cuotas.setValue(12)
        self._cuotas.setStyleSheet(input_style())
        self._interes = QDoubleSpinBox(); self._interes.setRange(0, 100)
        self._interes.setSuffix("%"); self._interes.setValue(12.0)
        self._interes.setStyleSheet(input_style())

        fl.addRow(make_label("Cuotas*", color=TEXT2, size=12), self._cuotas)
        fl.addRow(make_label("Interés anual*", color=TEXT2, size=12), self._interes)

        self._fin_frame.setVisible(False)
        cl.addWidget(self._fin_frame)

        # Botones
        btn_row = QHBoxLayout()
        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.setStyleSheet(btn_secondary())
        btn_limpiar.clicked.connect(self._limpiar)
        btn_row.addWidget(btn_limpiar)
        btn_row.addStretch()

        self._btn_deshacer = QPushButton("↩ Deshacer última")
        self._btn_deshacer.setStyleSheet(btn_danger())
        self._btn_deshacer.clicked.connect(self._deshacer)
        btn_row.addWidget(self._btn_deshacer)

        btn_ok = QPushButton("Registrar venta →")
        btn_ok.setStyleSheet(btn_primary())
        btn_ok.clicked.connect(self._registrar)
        btn_row.addWidget(btn_ok)
        cl.addLayout(btn_row)

        layout.addWidget(card)
        layout.addStretch()

    def _cargar_motos(self):
        self._moto_combo.clear()
        try:
            motos = self._ctrl.motos_disponibles()
            self._motos_map = {}
            for m in motos:
                label = f"[{m.id_moto}] {m.marca} {m.modelo} — ${m.precio:,.0f}"
                self._moto_combo.addItem(label, m.id_moto)
                self._motos_map[m.id_moto] = m
        except Exception as e:
            show_error(self, str(e))

    def _toggle_financiacion(self, tipo):
        self._fin_frame.setVisible(tipo == "financiado")

    def _limpiar(self):
        self._id_cliente.setValue(1)
        self._id_empleado.setValue(1)
        self._precio.setValue(0)
        self._tipo_pago.setCurrentIndex(0)
        self._cuotas.setValue(12)
        self._interes.setValue(12.0)
        self._cargar_motos()

    def _registrar(self):
        from model.VO.VentaVO import VentaVO
        from model.VO.FinanciacionVO import FinanciacionVO

        id_moto = self._moto_combo.currentData()
        if id_moto is None:
            show_error(self, "No hay motos disponibles para seleccionar."); return

        venta = VentaVO(
            id_venta=0,
            precio_final=self._precio.value(),
            tipo_pago=self._tipo_pago.currentText(),
            id_cliente=self._id_cliente.value(),
            id_moto=id_moto,
            id_empleado=self._id_empleado.value(),
        )

        financiacion = None
        if self._tipo_pago.currentText() == "financiado":
            financiacion = FinanciacionVO(
                id_financiacion=None,
                cuotas=self._cuotas.value(),
                interes=self._interes.value(),
            )

        try:
            id_v = self._ctrl.registrar_venta(venta, financiacion)
            show_ok(self, f"Venta #{id_v} registrada exitosamente.")
            self._cargar_motos()
            self.venta_registrada.emit()
        except Exception as e:
            show_error(self, str(e))

    def _deshacer(self):
        try:
            ok = self._ctrl.deshacer_venta()
            if ok:
                show_ok(self, "Última venta deshecha.")
                self._cargar_motos()
            else:
                show_error(self, "No hay ventas para deshacer.")
        except Exception as e:
            show_error(self, str(e))


# ── Ventas ───────────────────────────────────────────────────────────────────

class VentasPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        layout.addWidget(make_label("Historial de ventas", size=22, bold=True))

        # Filtros
        filter_card = QFrame(); filter_card.setStyleSheet(card_style())
        fl = QHBoxLayout(filter_card); fl.setContentsMargins(16, 14, 16, 14); fl.setSpacing(12)

        fl.addWidget(make_label("ID Cliente:", color=TEXT2))
        self._fil_cliente = QSpinBox(); self._fil_cliente.setRange(0, 99999)
        self._fil_cliente.setSpecialValueText("—")
        self._fil_cliente.setStyleSheet(input_style()); self._fil_cliente.setFixedWidth(90)
        fl.addWidget(self._fil_cliente)

        fl.addWidget(make_label("Desde:", color=TEXT2))
        self._fil_desde = QLineEdit("2024-01-01"); self._fil_desde.setFixedWidth(110)
        self._fil_desde.setStyleSheet(input_style())
        fl.addWidget(self._fil_desde)

        fl.addWidget(make_label("Hasta:", color=TEXT2))
        self._fil_hasta = QLineEdit("2025-12-31"); self._fil_hasta.setFixedWidth(110)
        self._fil_hasta.setStyleSheet(input_style())
        fl.addWidget(self._fil_hasta)

        btn_buscar = QPushButton("Filtrar")
        btn_buscar.setStyleSheet(btn_primary())
        btn_buscar.clicked.connect(self._filtrar)
        fl.addWidget(btn_buscar)
        fl.addStretch()
        layout.addWidget(filter_card)

        self._tbl = QTableWidget(0, 7)
        self._tbl.setStyleSheet(table_style())
        self._tbl.setHorizontalHeaderLabels(
            ["ID", "Fecha", "Moto", "Precio", "Tipo pago", "Cliente", "Empleado"])
        self._tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        layout.addWidget(self._tbl)

    def _filtrar(self):
        id_cli = self._fil_cliente.value()
        try:
            if id_cli > 0:
                ventas = self._ctrl.ventas_por_cliente(id_cli)
            else:
                ventas = self._ctrl.ventas_por_periodo(
                    self._fil_desde.text().strip(),
                    self._fil_hasta.text().strip()
                )
            self._populate(ventas)
        except Exception as e:
            show_error(self, str(e))

    def _populate(self, ventas):
        tipo_colors = {"contado": SUCCESS, "financiado": WARNING, "tarjeta": ACCENT}
        self._tbl.setRowCount(len(ventas))
        for i, v in enumerate(ventas):
            self._tbl.setItem(i, 0, QTableWidgetItem(str(v.id_venta)))
            self._tbl.setItem(i, 1, QTableWidgetItem(str(v.fecha_venta or "")))
            moto_txt = ""
            if v._moto_cache:
                moto_txt = f"{v._moto_cache.marca} {v._moto_cache.modelo}"
            self._tbl.setItem(i, 2, QTableWidgetItem(moto_txt))
            p = QTableWidgetItem(f"${v.precio_final:,.0f}" if v.precio_final else "")
            p.setForeground(QColor(SUCCESS))
            self._tbl.setItem(i, 3, p)
            tp = QTableWidgetItem(v.tipo_pago or "")
            tp.setForeground(QColor(tipo_colors.get(v.tipo_pago or "", TEXT2)))
            self._tbl.setItem(i, 4, tp)
            self._tbl.setItem(i, 5, QTableWidgetItem(str(v.id_cliente or "")))
            self._tbl.setItem(i, 6, QTableWidgetItem(str(v.id_empleado or "")))


# ── Categorías ───────────────────────────────────────────────────────────────

class CategoriasPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)
        layout.addWidget(make_label("Categorías de motos", size=22, bold=True))

        self._container = QWidget()
        self._flow = QVBoxLayout(self._container)
        self._flow.setSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(self._container)
        layout.addWidget(scroll)
        self._reload()

    def _reload(self):
        # Limpiar
        while self._flow.count():
            item = self._flow.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            cats = self._ctrl.listar_categorias()
        except Exception as e:
            show_error(self, str(e)); return

        for cat in cats:
            card = QFrame(); card.setStyleSheet(card_style())
            cl = QHBoxLayout(card); cl.setContentsMargins(20, 16, 20, 16)
            left = QVBoxLayout()
            left.addWidget(make_label(cat.nombre or "", size=14, bold=True))
            left.addWidget(make_label(cat.descripcion or "Sin descripción",
                                      color=TEXT2, size=12))
            cl.addLayout(left)
            cl.addStretch()
            badge = make_badge(f"#{cat.id_categoria}", ACCENT2)
            cl.addWidget(badge)
            self._flow.addWidget(card)

        self._flow.addStretch()


# ── Ventana principal ────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self._ctrl = controller
        self.setWindowTitle("MotoXpress — Sistema de Gestión")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 780)
        self.setStyleSheet(STYLE_GLOBAL)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self._sidebar = Sidebar()
        self._sidebar.page_changed.connect(self._switch_page)
        main_layout.addWidget(self._sidebar)

        # Páginas
        self._stack = QStackedWidget()
        self._stack.setStyleSheet(f"background: {BG};")

        self._pages = [
            DashboardPage(controller),
            MotosPage(controller),
            ClientesPage(controller),
            EmpleadosPage(controller),
            NuevaVentaPage(controller),
            VentasPage(controller),
            CategoriasPage(controller),
        ]
        for p in self._pages:
            self._stack.addWidget(p)

        # Conectar señal de venta registrada al dashboard
        self._pages[4].venta_registrada.connect(self._reload_dashboard)

        main_layout.addWidget(self._stack)

    def _switch_page(self, idx):
        self._stack.setCurrentIndex(idx)

    def _reload_dashboard(self):
        # Reconstruye el dashboard cuando se registra una venta
        old = self._pages[0]
        new = DashboardPage(self._ctrl)
        self._stack.removeWidget(old)
        old.deleteLater()
        self._stack.insertWidget(0, new)
        self._pages[0] = new


# ── Punto de entrada ─────────────────────────────────────────────────────────

def launch_ui(controller):

    app = QApplication(sys.argv)
    app.setApplicationName("MotoXpress")

    # Paleta global dark
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BG))
    palette.setColor(QPalette.WindowText, QColor(TEXT))
    palette.setColor(QPalette.Base, QColor(BG2))
    palette.setColor(QPalette.AlternateBase, QColor(BG3))
    palette.setColor(QPalette.Text, QColor(TEXT))
    palette.setColor(QPalette.Button, QColor(BG3))
    palette.setColor(QPalette.ButtonText, QColor(TEXT))
    palette.setColor(QPalette.Highlight, QColor(ACCENT))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    app.setPalette(palette)

    window = MainWindow(controller)
    window.show()
    sys.exit(app.exec_())
