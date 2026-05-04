# ─────────────────────────────────────────────
#  MotoXpress — Widgets reutilizables (v3)
# ─────────────────────────────────────────────
from PyQt5.QtWidgets import (
    QLabel, QFrame, QHBoxLayout, QVBoxLayout,
    QMessageBox, QPushButton, QWidget, QCheckBox,
    QApplication, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont

from ui.styles import (
    TEXT, TEXT2, TEXT3, ACCENT, ACCENT_L, ACCENT_XL, SUCCESS, SUCCESS_L,
    DANGER, DANGER_L, WARNING, WARNING_L, BORDER, BORDER2, PANEL, WHITE,
    OFF_WHITE, btn_primary, btn_secondary, btn_danger, STYLE_CHECKBOX,
    FONT_FAMILY
)


# ── Etiquetas ─────────────────────────────────────────────────────────────
def make_label(text, size=14, bold=False, color=TEXT, wrap=False, italic=False):
    lbl = QLabel(text)
    weight = "700" if bold else "400"
    style = (
        f"color: {color}; font-size: {size}px; "
        f"font-weight: {weight}; background: transparent; border: none; "
        f"font-family: {FONT_FAMILY};"
    )
    if italic:
        style += " font-style: italic;"
    lbl.setStyleSheet(style)
    if wrap:
        lbl.setWordWrap(True)
    return lbl


# ── Divisores ─────────────────────────────────────────────────────────────
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


# ── Badges ────────────────────────────────────────────────────────────────
def make_badge(text, color=ACCENT, bg=ACCENT_L, size=11):
    b = QLabel(text)
    b.setStyleSheet(f"""
        background: {bg};
        color: {color};
        border-radius: 5px;
        padding: 3px 10px;
        font-size: {size}px;
        font-weight: 600;
        font-family: {FONT_FAMILY};
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


# ── Diálogos mejorados ────────────────────────────────────────────────────
def _base_dialog(parent, title, msg, icon, btn_style_fn):
    """Helper interno para crear diálogos estilizados."""
    d = QMessageBox(parent)
    d.setWindowTitle(title)
    d.setText(msg)
    d.setIcon(icon)
    d.setStyleSheet(f"""
        QMessageBox {{
            background: {WHITE};
            color: {TEXT};
            font-family: {FONT_FAMILY};
        }}
        QLabel {{
            color: {TEXT};
            font-size: 14px;
            font-family: {FONT_FAMILY};
            background: transparent;
        }}
        QPushButton {{ {btn_style_fn()} }}
    """)
    return d


def show_error(parent, msg, title="Error"):
    d = _base_dialog(parent, title, msg, QMessageBox.Warning, btn_secondary)
    d.exec_()


def show_ok(parent, msg, title="Operación exitosa"):
    d = _base_dialog(parent, title, msg, QMessageBox.Information, btn_primary)
    d.exec_()


def show_confirm(parent, msg, title="Confirmar"):
    d = _base_dialog(parent, title, msg, QMessageBox.Question, btn_secondary)
    d.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    d.setDefaultButton(QMessageBox.No)
    return d.exec_() == QMessageBox.Yes


def mark_invalid(widget, invalid: bool):
    from ui.styles import STYLE_INPUT, STYLE_INPUT_ERROR
    widget.setStyleSheet(STYLE_INPUT_ERROR if invalid else STYLE_INPUT)


# ── StatCard — tarjeta de dashboard ──────────────────────────────────────
class StatCard(QFrame):
    """Tarjeta de estadística para el dashboard."""
    def __init__(self, icon, label, value, color=ACCENT, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border: 1.5px solid {BORDER};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(6)

        top = QHBoxLayout()
        icon_lbl = make_label(icon, size=20)
        top.addWidget(icon_lbl)
        top.addStretch()
        color_dot = QLabel()
        color_dot.setFixedSize(8, 8)
        color_dot.setStyleSheet(f"""
            background: {color};
            border-radius: 4px;
        """)
        top.addWidget(color_dot)
        layout.addLayout(top)

        layout.addSpacing(4)
        layout.addWidget(make_label(value, size=30, bold=True, color=color))
        layout.addWidget(make_label(label, size=12, color=TEXT3))


# ── SectionHeader ─────────────────────────────────────────────────────────
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


# ── EmptyState ────────────────────────────────────────────────────────────
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


# ── InlineToast — notificación no-modal ──────────────────────────────────
class InlineToast(QFrame):
    """
    Pequeña notificación inline que aparece debajo de una acción y
    desaparece sola después de unos segundos.
    Uso: toast = InlineToast(parent, "Cambios guardados", success=True)
         layout.addWidget(toast)
         toast.show_and_hide()
    """
    def __init__(self, parent=None, message="", success=True):
        super().__init__(parent)
        color  = SUCCESS if success else DANGER
        bg     = SUCCESS_L if success else DANGER_L
        prefix = "✓" if success else "✗"
        self.setStyleSheet(f"""
            QFrame {{
                background: {bg};
                border: 1px solid {color};
                border-radius: 8px;
                padding: 2px;
            }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)
        layout.addWidget(make_label(f"{prefix}  {message}", size=13, color=color))
        self.setVisible(False)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)

    def show_and_hide(self, ms=3000):
        self.setVisible(True)
        self._timer.start(ms)
