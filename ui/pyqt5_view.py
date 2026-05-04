import sys
from typing import Optional, List

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QSpinBox,
    QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QFrame, QScrollArea, QMessageBox, QHeaderView,
    QSizePolicy, QGraphicsDropShadowEffect, QDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QLinearGradient, QBrush,
    QPainter, QPen, QPixmap, QIcon, QFontDatabase
)

# ── Paleta de colores ─────────────────────────────────────────────────────────
BG        = "#0f172a"
BG2       = "#1e293b"
BG3       = "#263347"
CARD      = "#1e293b"
ACCENT    = "#3b82f6"
ACCENT_H  = "#2563eb"
SUCCESS   = "#22c55e"
DANGER    = "#ef4444"
WARNING   = "#f59e0b"
TEXT      = "#e2e8f0"
TEXT2     = "#94a3b8"
BORDER    = "#334155"
SELECTED  = "#2d3f5e"
ERROR_BG  = "#3b1a1a"
ERROR_BD  = "#7f1d1d"

# ── QSS Global centralizado ───────────────────────────────────────────────────
STYLE_GLOBAL = f"""
QWidget {{
    background-color: {BG};
    color: {TEXT};
    font-family: 'Segoe UI', 'Ubuntu', 'DejaVu Sans', sans-serif;
    font-size: 15px;
}}
QScrollBar:vertical {{
    background: {BG2};
    width: 7px;
    border-radius: 3px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 3px;
    min-height: 24px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: {BG2};
    height: 7px;
    border-radius: 3px;
}}
QScrollBar::handle:horizontal {{
    background: {BORDER};
    border-radius: 3px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    width: 0;
    height: 0;
    border: none;
}}
QToolTip {{
    background: {BG3};
    color: {TEXT};
    border: 1px solid {BORDER};
    padding: 4px 8px;
    font-size: 13px;
}}
"""

STYLE_INPUT = f"""
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    background: {BG3};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 10px 14px;
    color: {TEXT};
    font-size: 15px;
    selection-background-color: {SELECTED};
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {ACCENT};
    background: {BG2};
}}
QLineEdit:read-only {{
    color: {TEXT2};
}}
QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox::down-arrow {{
    width: 12px;
    height: 12px;
}}
QComboBox QAbstractItemView {{
    background: {BG3};
    border: 1px solid {BORDER};
    selection-background-color: {SELECTED};
    color: {TEXT};
    padding: 4px;
    outline: none;
}}
QComboBox QAbstractItemView::item {{
    padding: 8px 12px;
    min-height: 28px;
}}
"""

STYLE_INPUT_ERROR = f"""
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    background: {ERROR_BG};
    border: 1px solid {ERROR_BD};
    border-radius: 6px;
    padding: 10px 14px;
    color: {TEXT};
    font-size: 15px;
}}
"""

STYLE_TABLE = f"""
QTableWidget {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 6px;
    gridline-color: {BORDER};
    color: {TEXT};
    font-size: 14px;
    outline: none;
}}
QHeaderView::section {{
    background: {BG3};
    color: {TEXT2};
    border: none;
    border-bottom: 1px solid {BORDER};
    border-right: 1px solid {BORDER};
    padding: 10px 14px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}}
QHeaderView::section:last {{
    border-right: none;
}}
QTableWidget::item {{
    padding: 10px 14px;
    border-bottom: 1px solid {BORDER};
}}
QTableWidget::item:selected {{
    background: {SELECTED};
    color: {TEXT};
}}
QTableCornerButton::section {{
    background: {BG3};
    border: none;
}}
"""

def _card_style():
    return f"""
        QFrame {{
            background-color: {CARD};
            border: 1px solid {BORDER};
            border-radius: 8px;
        }}
    """

def _btn_primary():
    return f"""
        QPushButton {{
            background-color: {ACCENT};
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 10px 22px;
            font-weight: 600;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {ACCENT_H};
        }}
        QPushButton:pressed {{
            background-color: #1d4ed8;
        }}
        QPushButton:disabled {{
            background-color: {BORDER};
            color: {TEXT2};
        }}
    """

def _btn_secondary():
    return f"""
        QPushButton {{
            background-color: transparent;
            color: {TEXT2};
            border: 1px solid {BORDER};
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {BG3};
            color: {TEXT};
            border-color: {TEXT2};
        }}
        QPushButton:pressed {{
            background-color: {SELECTED};
        }}
    """

def _btn_danger():
    return f"""
        QPushButton {{
            background-color: transparent;
            color: {DANGER};
            border: 1px solid {DANGER};
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: rgba(239, 68, 68, 0.10);
        }}
    """


# ── Helpers de UI ─────────────────────────────────────────────────────────────

def make_label(text, size=15, bold=False, color=TEXT, wrap=False):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"color: {color}; font-size: {size}px; "
        f"font-weight: {'600' if bold else '400'}; background: transparent; border: none;"
    )
    if wrap:
        lbl.setWordWrap(True)
    return lbl


def make_divider():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet(f"background: {BORDER}; border: none; max-height: 1px;")
    line.setFixedHeight(1)
    return line


def make_badge(text, color=ACCENT):
    b = QLabel(text)
    b.setStyleSheet(f"""
        background: transparent;
        color: {color};
        border: 1px solid {color};
        border-radius: 4px;
        padding: 3px 10px;
        font-size: 12px;
        font-weight: 600;
    """)
    b.setAlignment(Qt.AlignCenter)
    return b


def show_error(parent, msg):
    d = QMessageBox(parent)
    d.setWindowTitle("Error")
    d.setText(msg)
    d.setIcon(QMessageBox.Warning)
    d.setStyleSheet(
        f"QMessageBox {{ background: {BG2}; color: {TEXT}; }} "
        f"QPushButton {{ {_btn_secondary()} }}"
    )
    d.exec_()


def show_ok(parent, msg):
    d = QMessageBox(parent)
    d.setWindowTitle("Operación exitosa")
    d.setText(msg)
    d.setIcon(QMessageBox.Information)
    d.setStyleSheet(
        f"QMessageBox {{ background: {BG2}; color: {TEXT}; }} "
        f"QPushButton {{ {_btn_primary()} }}"
    )
    d.exec_()


def _mark_invalid(widget, invalid: bool):
    """Aplica/quita el estilo de error en un campo de entrada."""
    widget.setStyleSheet(STYLE_INPUT_ERROR if invalid else STYLE_INPUT)


# ── Sidebar ───────────────────────────────────────────────────────────────────

class Sidebar(QWidget):
    page_changed = pyqtSignal(int)

    ITEMS = [
        ("Dashboard",    "🏠"),
        ("Motos",        "🏍"),
        ("Clientes",     "👥"),
        ("Empleados",    "💼"),
        ("Nueva Venta",  "🧾"),
        ("Ventas",       "📊"),
        ("Categorías",   "🏷"),
    ]

    def __init__(self):
        super().__init__()
        self.setFixedWidth(210)
        self.setStyleSheet(
            f"QWidget {{ background: {BG2}; border-right: 1px solid {BORDER}; }}"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo
        logo_wrap = QWidget()
        logo_wrap.setFixedHeight(68)
        logo_wrap.setStyleSheet(
            f"background: {BG2}; border-bottom: 1px solid {BORDER}; border-right: none;"
        )
        ll = QHBoxLayout(logo_wrap)
        ll.setContentsMargins(18, 0, 18, 0)
        ll.setSpacing(10)
        icon_lbl = make_label("🏍", size=20)
        title_lbl = make_label("MotoXpress", size=15, bold=True)
        ll.addWidget(icon_lbl)
        ll.addWidget(title_lbl)
        ll.addStretch()
        layout.addWidget(logo_wrap)

        layout.addSpacing(10)

        self._buttons = []
        for i, (label, emoji) in enumerate(self.ITEMS):
            btn = QPushButton(f"  {emoji}   {label}")
            btn.setCheckable(True)
            btn.setFixedHeight(42)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(self._btn_style(False))
            btn.clicked.connect(lambda _, idx=i: self._select(idx))
            layout.addWidget(btn)
            self._buttons.append(btn)

        layout.addStretch()

        ver = make_label("v1.0.0", size=11, color=TEXT2)
        ver.setContentsMargins(18, 0, 0, 14)
        layout.addWidget(ver)

        self._select(0)

    def _btn_style(self, active):
        if active:
            return f"""
                QPushButton {{
                    background: {SELECTED};
                    color: {TEXT};
                    border: none;
                    border-left: 3px solid {ACCENT};
                    text-align: left;
                    padding: 0 18px;
                    font-size: 14px;
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
                padding: 0 18px;
                font-size: 14px;
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


# ── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        layout.addWidget(make_label("Dashboard", size=22, bold=True))
        layout.addWidget(make_label("Resumen del concesionario", color=TEXT2, size=14))

        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)

        try:
            motos     = self._ctrl.motos_disponibles()
            clientes  = self._ctrl.listar_clientes()
            empleados = self._ctrl.listar_empleados()
            cats      = self._ctrl.listar_categorias()
        except Exception:
            motos, clientes, empleados, cats = [], [], [], []

        cards_data = [
            ("🏍", "Motos disponibles", str(len(motos)),    ACCENT),
            ("👥", "Clientes",          str(len(clientes)), SUCCESS),
            ("💼", "Empleados",         str(len(empleados)),WARNING),
            ("🏷", "Categorías",        str(len(cats)),     TEXT2),
        ]
        for emoji, label, value, color in cards_data:
            stats_row.addWidget(self._stat_card(emoji, label, value, color))
        layout.addLayout(stats_row)

        layout.addWidget(make_label("Motos disponibles", size=15, bold=True))
        tbl = self._motos_table(motos[:8])
        layout.addWidget(tbl)
        layout.addStretch()

    def _stat_card(self, emoji, label, value, color):
        card = QFrame()
        card.setStyleSheet(_card_style())
        vl = QVBoxLayout(card)
        vl.setContentsMargins(20, 18, 20, 18)
        vl.setSpacing(6)
        top = QHBoxLayout()
        top.addWidget(make_label(emoji, size=18))
        top.addStretch()
        vl.addLayout(top)
        vl.addWidget(make_label(value, size=26, bold=True, color=color))
        vl.addWidget(make_label(label, size=12, color=TEXT2))
        return card

    def _motos_table(self, motos):
        tbl = QTableWidget(len(motos), 6)
        tbl.setStyleSheet(STYLE_TABLE)
        tbl.setHorizontalHeaderLabels(["ID", "Marca", "Modelo", "Año", "Precio", "Estado"])
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        tbl.setSelectionBehavior(QTableWidget.SelectRows)
        tbl.verticalHeader().setVisible(False)
        tbl.setFocusPolicy(Qt.NoFocus)
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


# ── Motos ─────────────────────────────────────────────────────────────────────

class MotosPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        header = QHBoxLayout()
        header.addWidget(make_label("Motos disponibles", size=22, bold=True))
        header.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("Buscar por marca o modelo…")
        self._search.setFixedWidth(240)
        self._search.setStyleSheet(STYLE_INPUT)
        self._search.textChanged.connect(self._filter)
        header.addWidget(self._search)

        btn_reg = QPushButton("+ Registrar moto")
        btn_reg.setStyleSheet(_btn_primary())
        btn_reg.setCursor(Qt.PointingHandCursor)
        btn_reg.clicked.connect(self._form_registrar)
        header.addWidget(btn_reg)
        layout.addLayout(header)

        self._tbl = QTableWidget(0, 7)
        self._tbl.setStyleSheet(STYLE_TABLE)
        self._tbl.setHorizontalHeaderLabels(
            ["ID", "VIN", "Marca", "Modelo", "Año", "Precio", "Estado"])
        self._tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        self._tbl.setFocusPolicy(Qt.NoFocus)
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
            self._tbl.setItem(i, 5, p)
            e = QTableWidgetItem(m.estado or "")
            e.setForeground(QColor(SUCCESS if m.estado == 'disponible' else WARNING))
            self._tbl.setItem(i, 6, e)

    def _form_registrar(self):
        dialog = _MotoDialog(self, self._ctrl)
        if dialog.exec_() == QDialog.Accepted:
            self._reload()


class _MotoDialog(QDialog):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self._ctrl = controller
        self.setWindowTitle("Registrar nueva moto")
        self.setFixedSize(460, 500)
        self.setStyleSheet(f"QDialog {{ background: {BG2}; }} {STYLE_INPUT}")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)
        layout.addWidget(make_label("Nueva moto", size=18, bold=True))
        layout.addWidget(make_divider())

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self._vin    = QLineEdit(); self._vin.setStyleSheet(STYLE_INPUT)
        self._marca  = QLineEdit(); self._marca.setStyleSheet(STYLE_INPUT)
        self._model  = QLineEdit(); self._model.setStyleSheet(STYLE_INPUT)
        self._anio   = QSpinBox();  self._anio.setRange(1990, 2030); self._anio.setValue(2024)
        self._anio.setStyleSheet(STYLE_INPUT)
        self._precio = QDoubleSpinBox(); self._precio.setRange(0, 99999999)
        self._precio.setPrefix("$"); self._precio.setStyleSheet(STYLE_INPUT)
        self._color  = QLineEdit(); self._color.setStyleSheet(STYLE_INPUT)

        for lbl, w in [("VIN", self._vin), ("Marca", self._marca),
                        ("Modelo", self._model), ("Año", self._anio),
                        ("Precio", self._precio), ("Color", self._color)]:
            form.addRow(make_label(lbl, color=TEXT2, size=13), w)
        layout.addLayout(form)
        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(_btn_secondary())
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_cancel)
        btn_row.addStretch()
        btn = QPushButton("Registrar")
        btn.setStyleSheet(_btn_primary())
        btn.clicked.connect(self._save)
        btn_row.addWidget(btn)
        layout.addLayout(btn_row)

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
            self.accept()
        except Exception as e:
            show_error(self, str(e))


# ── Clientes ──────────────────────────────────────────────────────────────────

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
        self._search.setStyleSheet(STYLE_INPUT)
        self._search.returnPressed.connect(self._buscar_cedula)
        header.addWidget(self._search)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.setStyleSheet(_btn_secondary())
        btn_buscar.clicked.connect(self._buscar_cedula)
        header.addWidget(btn_buscar)

        btn_reg = QPushButton("+ Registrar cliente")
        btn_reg.setStyleSheet(_btn_primary())
        btn_reg.clicked.connect(self._form_registrar)
        header.addWidget(btn_reg)
        layout.addLayout(header)

        self._tbl = QTableWidget(0, 6)
        self._tbl.setStyleSheet(STYLE_TABLE)
        self._tbl.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Apellido", "Cédula", "Teléfono", "Email"])
        self._tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        self._tbl.setFocusPolicy(Qt.NoFocus)
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
        if dlg.exec_() == QDialog.Accepted:
            self._reload()


class _ClienteDialog(QDialog):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self._ctrl = controller
        self.setWindowTitle("Registrar cliente")
        self.setFixedSize(440, 440)
        self.setStyleSheet(f"QDialog {{ background: {BG2}; }} {STYLE_INPUT}")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)
        layout.addWidget(make_label("Nuevo cliente", size=18, bold=True))
        layout.addWidget(make_divider())

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self._nombre   = QLineEdit(); self._nombre.setStyleSheet(STYLE_INPUT)
        self._apellido = QLineEdit(); self._apellido.setStyleSheet(STYLE_INPUT)
        self._cedula   = QLineEdit(); self._cedula.setStyleSheet(STYLE_INPUT)
        self._telefono = QLineEdit(); self._telefono.setStyleSheet(STYLE_INPUT)
        self._email    = QLineEdit(); self._email.setStyleSheet(STYLE_INPUT)

        for lbl, w in [("Nombre *", self._nombre), ("Apellido *", self._apellido),
                        ("Cédula *", self._cedula), ("Teléfono", self._telefono),
                        ("Email", self._email)]:
            form.addRow(make_label(lbl, color=TEXT2, size=13), w)
        layout.addLayout(form)
        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(_btn_secondary())
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_cancel)
        btn_row.addStretch()
        btn = QPushButton("Registrar")
        btn.setStyleSheet(_btn_primary())
        btn.clicked.connect(self._save)
        btn_row.addWidget(btn)
        layout.addLayout(btn_row)

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
            self.accept()
        except Exception as e:
            show_error(self, str(e))


# ── Empleados ─────────────────────────────────────────────────────────────────

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
        combo.setStyleSheet(STYLE_INPUT)
        combo.setFixedWidth(180)
        combo.currentTextChanged.connect(self._filtrar_rol)
        header.addWidget(combo)
        layout.addLayout(header)

        self._tbl = QTableWidget(0, 5)
        self._tbl.setStyleSheet(STYLE_TABLE)
        self._tbl.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Rol", "Email"])
        self._tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        self._tbl.setFocusPolicy(Qt.NoFocus)
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


# ── Nueva Venta ───────────────────────────────────────────────────────────────

class NuevaVentaPage(QWidget):
    venta_registrada = pyqtSignal()

    # Campos obligatorios (widget, nombre visible)
    _REQUIRED_FIELDS = []

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
        layout.addWidget(make_label(
            "Todos los campos marcados con * son obligatorios.",
            color=TEXT2, size=13))

        # ── Card principal ──
        card = QFrame()
        card.setStyleSheet(_card_style())
        cl = QVBoxLayout(card)
        cl.setContentsMargins(28, 28, 28, 28)
        cl.setSpacing(18)

        form = QFormLayout()
        form.setSpacing(14)
        form.setLabelAlignment(Qt.AlignRight)

        # ID Cliente
        self._id_cliente = QSpinBox()
        self._id_cliente.setRange(1, 99999)
        self._id_cliente.setStyleSheet(STYLE_INPUT)
        self._err_cliente = make_label("", size=12, color=DANGER)
        self._err_cliente.setVisible(False)
        form.addRow(make_label("ID Cliente *", color=TEXT2, size=13), self._id_cliente)
        form.addRow("", self._err_cliente)

        # Moto
        self._moto_combo = QComboBox()
        self._moto_combo.setStyleSheet(STYLE_INPUT)
        self._cargar_motos()
        self._err_moto = make_label("", size=12, color=DANGER)
        self._err_moto.setVisible(False)
        form.addRow(make_label("Moto *", color=TEXT2, size=13), self._moto_combo)
        form.addRow("", self._err_moto)

        # ID Empleado
        self._id_empleado = QSpinBox()
        self._id_empleado.setRange(1, 99999)
        self._id_empleado.setStyleSheet(STYLE_INPUT)
        self._err_empleado = make_label("", size=12, color=DANGER)
        self._err_empleado.setVisible(False)
        form.addRow(make_label("ID Empleado *", color=TEXT2, size=13), self._id_empleado)
        form.addRow("", self._err_empleado)

        # Precio final
        self._precio = QDoubleSpinBox()
        self._precio.setRange(0, 99999999)
        self._precio.setPrefix("$")
        self._precio.setStyleSheet(STYLE_INPUT)
        self._err_precio = make_label("", size=12, color=DANGER)
        self._err_precio.setVisible(False)
        form.addRow(make_label("Precio final *", color=TEXT2, size=13), self._precio)
        form.addRow("", self._err_precio)

        # Tipo de pago
        self._tipo_pago = QComboBox()
        self._tipo_pago.addItems(["contado", "financiado", "tarjeta"])
        self._tipo_pago.setStyleSheet(STYLE_INPUT)
        self._tipo_pago.currentTextChanged.connect(self._toggle_financiacion)
        form.addRow(make_label("Tipo de pago *", color=TEXT2, size=13), self._tipo_pago)

        cl.addLayout(form)

        # ── Panel financiación ──
        self._fin_frame = QFrame()
        self._fin_frame.setStyleSheet(f"""
            QFrame {{
                background: {BG3};
                border: 1px solid {BORDER};
                border-radius: 6px;
            }}
        """)
        fl = QFormLayout(self._fin_frame)
        fl.setContentsMargins(20, 18, 20, 18)
        fl.setSpacing(12)
        fl.setLabelAlignment(Qt.AlignRight)

        fin_title = make_label("Plan de financiación", size=14, bold=True, color=ACCENT)
        fl.addRow(fin_title)

        self._cuotas = QSpinBox()
        self._cuotas.setRange(1, 60)
        self._cuotas.setValue(12)
        self._cuotas.setStyleSheet(STYLE_INPUT)

        self._interes = QDoubleSpinBox()
        self._interes.setRange(0, 100)
        self._interes.setSuffix("%")
        self._interes.setValue(12.0)
        self._interes.setStyleSheet(STYLE_INPUT)

        fl.addRow(make_label("Cuotas *", color=TEXT2, size=13), self._cuotas)
        fl.addRow(make_label("Interés anual *", color=TEXT2, size=13), self._interes)

        self._fin_frame.setVisible(False)
        cl.addWidget(self._fin_frame)

        # ── Botones ──
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.setStyleSheet(_btn_secondary())
        btn_limpiar.setCursor(Qt.PointingHandCursor)
        btn_limpiar.clicked.connect(self._limpiar)
        btn_row.addWidget(btn_limpiar)

        btn_row.addStretch()

        self._btn_deshacer = QPushButton("↩ Deshacer última")
        self._btn_deshacer.setStyleSheet(_btn_danger())
        self._btn_deshacer.setCursor(Qt.PointingHandCursor)
        self._btn_deshacer.clicked.connect(self._deshacer)
        btn_row.addWidget(self._btn_deshacer)

        btn_ok = QPushButton("Registrar venta →")
        btn_ok.setStyleSheet(_btn_primary())
        btn_ok.setCursor(Qt.PointingHandCursor)
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
        # Limpiar feedback visual
        for w in (self._id_cliente, self._id_empleado, self._precio, self._moto_combo):
            w.setStyleSheet(STYLE_INPUT)
        for lbl in (self._err_cliente, self._err_empleado, self._err_precio, self._err_moto):
            lbl.setVisible(False)

    def _validate(self):
        """Valida todos los campos obligatorios. Retorna True si todo es correcto."""
        ok = True

        # ID Cliente >= 1 (mínimo del spinbox, siempre cumplido; validar lógicamente)
        if self._id_cliente.value() < 1:
            self._id_cliente.setStyleSheet(STYLE_INPUT_ERROR)
            self._err_cliente.setText("El ID de cliente es obligatorio.")
            self._err_cliente.setVisible(True)
            ok = False
        else:
            self._id_cliente.setStyleSheet(STYLE_INPUT)
            self._err_cliente.setVisible(False)

        # Moto seleccionada
        if self._moto_combo.currentData() is None:
            self._moto_combo.setStyleSheet(STYLE_INPUT_ERROR)
            self._err_moto.setText("Selecciona una moto disponible.")
            self._err_moto.setVisible(True)
            ok = False
        else:
            self._moto_combo.setStyleSheet(STYLE_INPUT)
            self._err_moto.setVisible(False)

        # ID Empleado
        if self._id_empleado.value() < 1:
            self._id_empleado.setStyleSheet(STYLE_INPUT_ERROR)
            self._err_empleado.setText("El ID de empleado es obligatorio.")
            self._err_empleado.setVisible(True)
            ok = False
        else:
            self._id_empleado.setStyleSheet(STYLE_INPUT)
            self._err_empleado.setVisible(False)

        # Precio > 0
        if self._precio.value() <= 0:
            self._precio.setStyleSheet(STYLE_INPUT_ERROR)
            self._err_precio.setText("El precio debe ser mayor que cero.")
            self._err_precio.setVisible(True)
            ok = False
        else:
            self._precio.setStyleSheet(STYLE_INPUT)
            self._err_precio.setVisible(False)

        return ok

    def _registrar(self):
        from model.VO.VentaVO import VentaVO
        from model.VO.FinanciacionVO import FinanciacionVO

        if not self._validate():
            return

        id_moto = self._moto_combo.currentData()

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


# ── Ventas ────────────────────────────────────────────────────────────────────

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

        # ── Filtros ──
        filter_card = QFrame()
        filter_card.setStyleSheet(_card_style())
        fl = QHBoxLayout(filter_card)
        fl.setContentsMargins(18, 14, 18, 14)
        fl.setSpacing(14)

        fl.addWidget(make_label("ID Cliente:", color=TEXT2, size=13))
        self._fil_cliente = QSpinBox()
        self._fil_cliente.setRange(0, 99999)
        self._fil_cliente.setSpecialValueText("—")
        self._fil_cliente.setStyleSheet(STYLE_INPUT)
        self._fil_cliente.setFixedWidth(88)
        fl.addWidget(self._fil_cliente)

        # Separador visual
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet(f"color: {BORDER}; background: {BORDER};")
        sep.setFixedWidth(1)
        fl.addWidget(sep)

        fl.addWidget(make_label("Desde:", color=TEXT2, size=13))
        self._fil_desde = QLineEdit("2024-01-01")
        self._fil_desde.setFixedWidth(112)
        self._fil_desde.setStyleSheet(STYLE_INPUT)
        self._fil_desde.setPlaceholderText("AAAA-MM-DD")
        fl.addWidget(self._fil_desde)

        fl.addWidget(make_label("Hasta:", color=TEXT2, size=13))
        self._fil_hasta = QLineEdit("2025-12-31")
        self._fil_hasta.setFixedWidth(112)
        self._fil_hasta.setStyleSheet(STYLE_INPUT)
        self._fil_hasta.setPlaceholderText("AAAA-MM-DD")
        fl.addWidget(self._fil_hasta)

        btn_buscar = QPushButton("Filtrar")
        btn_buscar.setStyleSheet(_btn_primary())
        btn_buscar.setCursor(Qt.PointingHandCursor)
        btn_buscar.clicked.connect(self._filtrar)
        fl.addWidget(btn_buscar)

        btn_reset = QPushButton("Limpiar")
        btn_reset.setStyleSheet(_btn_secondary())
        btn_reset.setCursor(Qt.PointingHandCursor)
        btn_reset.clicked.connect(self._reset_filtros)
        fl.addWidget(btn_reset)

        fl.addStretch()
        layout.addWidget(filter_card)

        # ── Tabla ──
        self._tbl = QTableWidget(0, 7)
        self._tbl.setStyleSheet(STYLE_TABLE)
        self._tbl.setHorizontalHeaderLabels(
            ["ID", "Fecha", "Moto", "Precio", "Tipo pago", "Cliente", "Empleado"])
        self._tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        self._tbl.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(self._tbl)

        # Carga inicial: todas las ventas por periodo por defecto
        self._filtrar()

    def _reset_filtros(self):
        self._fil_cliente.setValue(0)
        self._fil_desde.setText("2024-01-01")
        self._fil_hasta.setText("2025-12-31")
        self._filtrar()

    def _filtrar(self):
        """
        Si hay un ID de cliente seleccionado (> 0), filtra por cliente.
        Si no, filtra por rango de fechas.
        Ambos modos son exclusivos: cliente tiene prioridad.
        """
        id_cli = self._fil_cliente.value()
        try:
            if id_cli > 0:
                ventas = self._ctrl.ventas_por_cliente(id_cli)
            else:
                desde = self._fil_desde.text().strip()
                hasta = self._fil_hasta.text().strip()
                ventas = self._ctrl.ventas_por_periodo(desde, hasta)
            self._populate(ventas)
        except Exception as e:
            show_error(self, str(e))

    def _populate(self, ventas):
        tipo_colors = {
            "contado":    SUCCESS,
            "financiado": WARNING,
            "tarjeta":    ACCENT,
        }
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


# ── Categorías ────────────────────────────────────────────────────────────────

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
        while self._flow.count():
            item = self._flow.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            cats = self._ctrl.listar_categorias()
        except Exception as e:
            show_error(self, str(e)); return

        for cat in cats:
            card = QFrame()
            card.setStyleSheet(_card_style())
            cl = QHBoxLayout(card)
            cl.setContentsMargins(22, 16, 22, 16)
            cl.setSpacing(16)
            left = QVBoxLayout()
            left.setSpacing(4)
            left.addWidget(make_label(cat.nombre or "", size=15, bold=True))
            left.addWidget(make_label(cat.descripcion or "Sin descripción",
                                      color=TEXT2, size=13))
            cl.addLayout(left)
            cl.addStretch()
            badge = make_badge(f"#{cat.id_categoria}")
            cl.addWidget(badge)
            self._flow.addWidget(card)

        self._flow.addStretch()


# ── Ventana principal ─────────────────────────────────────────────────────────

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
        old = self._pages[0]
        new = DashboardPage(self._ctrl)
        self._stack.removeWidget(old)
        old.deleteLater()
        self._stack.insertWidget(0, new)
        self._pages[0] = new


# ── Punto de entrada ──────────────────────────────────────────────────────────

def launch_ui(controller):
    app = QApplication(sys.argv)
    app.setApplicationName("MotoXpress")
    app.setStyle("Fusion")  # fuerza QSS en Windows sin interferencia del tema del SO

    palette = QPalette()
    palette.setColor(QPalette.Window,          QColor(BG))
    palette.setColor(QPalette.WindowText,      QColor(TEXT))
    palette.setColor(QPalette.Base,            QColor(BG2))
    palette.setColor(QPalette.AlternateBase,   QColor(BG3))
    palette.setColor(QPalette.Text,            QColor(TEXT))
    palette.setColor(QPalette.Button,          QColor(BG3))
    palette.setColor(QPalette.ButtonText,      QColor(TEXT))
    palette.setColor(QPalette.Highlight,       QColor(ACCENT))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    window = MainWindow(controller)
    window.show()
    sys.exit(app.exec_())