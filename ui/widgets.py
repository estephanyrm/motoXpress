# ─────────────────────────────────────────────
#  MotoXpress — Widgets reutilizables
# ─────────────────────────────────────────────
from PyQt5.QtWidgets import (
    QLabel, QFrame, QHBoxLayout, QVBoxLayout,
    QMessageBox, QPushButton, QWidget, QCheckBox,
    QApplication
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont

from ui.styles import (
    TEXT, TEXT2, TEXT3, ACCENT, ACCENT_L, SUCCESS, SUCCESS_L,
    DANGER, DANGER_L, WARNING, WARNING_L, BORDER, PANEL, WHITE,
    OFF_WHITE, btn_primary, btn_secondary, STYLE_CHECKBOX
)


def make_label(text, size=14, bold=False, color=TEXT, wrap=False, italic=False):
    lbl = QLabel(text)
    weight = "700" if bold else ("400" if not italic else "400")
    style = (
        f"color: {color}; font-size: {size}px; "
        f"font-weight: {weight}; background: transparent; border: none;"
    )
    if italic:
        style += " font-style: italic;"
    lbl.setStyleSheet(style)
    if wrap:
        lbl.setWordWrap(True)
    return lbl


def make_divider(vertical=False):
    line = QFrame()
    if vertical:
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet(f"background: {BORDER}; border: none; max-width: 1px;")
        line.setFixedWidth(1)
    else:
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background: {BORDER}; border: none; max-height: 1px;")
        line.setFixedHeight(1)
    return line


def make_badge(text, color=ACCENT, bg=ACCENT_L, size=11):
    b = QLabel(text)
    b.setStyleSheet(f"""
        background: {bg};
        color: {color};
        border-radius: 5px;
        padding: 3px 9px;
        font-size: {size}px;
        font-weight: 600;
    """)
    b.setAlignment(Qt.AlignCenter)
    return b


def make_status_badge(estado: str):
    mapping = {
        "disponible": (SUCCESS,  SUCCESS_L,  "Disponible"),
        "vendida":    (DANGER,   DANGER_L,   "Vendida"),
        "reservada":  (WARNING,  WARNING_L,  "Reservada"),
    }
    color, bg, label = mapping.get(estado, (TEXT2, PANEL, estado.capitalize()))
    return make_badge(label, color=color, bg=bg)


def make_tipo_pago_badge(tipo: str):
    mapping = {
        "contado":    (SUCCESS,  SUCCESS_L),
        "financiado": (WARNING,  WARNING_L),
        "tarjeta":    (ACCENT,   ACCENT_L),
    }
    color, bg = mapping.get(tipo, (TEXT2, PANEL))
    return make_badge(tipo.capitalize(), color=color, bg=bg)


def make_checkbox(text=""):
    cb = QCheckBox(text)
    cb.setStyleSheet(STYLE_CHECKBOX)
    return cb


def show_error(parent, msg):
    d = QMessageBox(parent)
    d.setWindowTitle("Error")
    d.setText(msg)
    d.setIcon(QMessageBox.Warning)
    d.setStyleSheet(f"""
        QMessageBox {{ background: {WHITE}; color: {TEXT}; }}
        QLabel {{ color: {TEXT}; font-size: 14px; }}
        QPushButton {{ {btn_secondary()} }}
    """)
    d.exec_()


def show_ok(parent, msg, title="Operación exitosa"):
    d = QMessageBox(parent)
    d.setWindowTitle(title)
    d.setText(msg)
    d.setIcon(QMessageBox.Information)
    d.setStyleSheet(f"""
        QMessageBox {{ background: {WHITE}; color: {TEXT}; }}
        QLabel {{ color: {TEXT}; font-size: 14px; }}
        QPushButton {{ {btn_primary()} }}
    """)
    d.exec_()


def show_confirm(parent, msg, title="Confirmar"):
    d = QMessageBox(parent)
    d.setWindowTitle(title)
    d.setText(msg)
    d.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    d.setDefaultButton(QMessageBox.No)
    d.setStyleSheet(f"""
        QMessageBox {{ background: {WHITE}; color: {TEXT}; }}
        QLabel {{ color: {TEXT}; font-size: 14px; }}
        QPushButton {{ {btn_secondary()} }}
    """)
    return d.exec_() == QMessageBox.Yes


def mark_invalid(widget, invalid: bool):
    from ui.styles import STYLE_INPUT, STYLE_INPUT_ERROR
    widget.setStyleSheet(STYLE_INPUT_ERROR if invalid else STYLE_INPUT)


class StatCard(QFrame):
    """Tarjeta de estadística para el dashboard."""
    def __init__(self, icon, label, value, color=ACCENT, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border: 1.5px solid {BORDER};
                border-radius: 10px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)

        top = QHBoxLayout()
        icon_lbl = make_label(icon, size=20)
        top.addWidget(icon_lbl)
        top.addStretch()
        layout.addLayout(top)

        layout.addWidget(make_label(value, size=28, bold=True, color=color))
        layout.addWidget(make_label(label, size=12, color=TEXT2))


class SectionHeader(QWidget):
    """Encabezado de sección con título y subtítulo."""
    def __init__(self, title, subtitle="", parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(make_label(title, size=20, bold=True))
        if subtitle:
            layout.addWidget(make_label(subtitle, size=13, color=TEXT2))


class EmptyState(QWidget):
    """Mensaje cuando no hay datos."""
    def __init__(self, icon="📭", message="Sin resultados", parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        layout.addWidget(make_label(icon, size=36), alignment=Qt.AlignCenter)
        layout.addWidget(make_label(message, size=14, color=TEXT3),
                         alignment=Qt.AlignCenter)
