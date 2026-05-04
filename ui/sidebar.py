# ─────────────────────────────────────────────
#  MotoXpress — Sidebar
# ─────────────────────────────────────────────
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from ui.styles import (
    SIDEBAR_BG, SIDEBAR_T, SIDEBAR_A, SIDEBAR_HV, SIDEBAR_SEL,
    ACCENT, BORDER, WHITE, TEXT2
)
from ui.widgets import make_label


class Sidebar(QWidget):
    page_changed = pyqtSignal(int)

    ITEMS = [
        ("Dashboard",    "⬛", "Resumen general"),
        ("Motos",        "⬛", "Inventario"),
        ("Clientes",     "⬛", "Base de clientes"),
        ("Empleados",    "⬛", "Personal"),
        ("Nueva Venta",  "⬛", "Registrar venta"),
        ("Ventas",       "⬛", "Historial"),
        ("Categorías",   "⬛", "Tipos de moto"),
    ]

    # Íconos Unicode simples (no emoji grandes)
    ICONS = ["◈", "◉", "◎", "◆", "◇", "◈", "◐"]

    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)
        self.setObjectName("sidebar")
        self.setStyleSheet(f"QWidget {{ background: {SIDEBAR_BG}; border: none; }}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Logo ──
        logo_wrap = QWidget()
        logo_wrap.setFixedHeight(70)
        logo_wrap.setStyleSheet(
            f"background: {SIDEBAR_BG}; border-bottom: 1px solid rgba(255,255,255,0.06);"
        )
        ll = QHBoxLayout(logo_wrap)
        ll.setContentsMargins(20, 0, 20, 0)
        ll.setSpacing(10)

        dot = QLabel("●")
        dot.setStyleSheet(f"color: {ACCENT}; font-size: 10px; background: transparent;")
        title_lbl = QLabel("MotoXpress")
        title_lbl.setStyleSheet(
            f"color: {WHITE}; font-size: 15px; font-weight: 700; "
            f"letter-spacing: 0.5px; background: transparent;"
        )
        ll.addWidget(dot)
        ll.addWidget(title_lbl)
        ll.addStretch()
        layout.addWidget(logo_wrap)

        layout.addSpacing(16)

        # ── Grupo nav ──
        nav_label = QLabel("NAVEGACIÓN")
        nav_label.setStyleSheet(
            f"color: rgba(168,176,196,0.45); font-size: 10px; font-weight: 700; "
            f"letter-spacing: 1.2px; background: transparent; padding: 0 20px;"
        )
        layout.addWidget(nav_label)
        layout.addSpacing(8)

        self._buttons = []
        for i, (label, _, _hint) in enumerate(self.ITEMS):
            btn = self._make_btn(i, label)
            layout.addWidget(btn)
            self._buttons.append(btn)

        layout.addStretch()

        # ── Footer ──
        ver = QLabel("v2.0")
        ver.setStyleSheet(
            f"color: rgba(168,176,196,0.35); font-size: 11px; "
            f"background: transparent; padding: 16px 22px;"
        )
        layout.addWidget(ver)

        self._current = -1
        self._select(0)

    def _make_btn(self, idx, label):
        icon = self.ICONS[idx]
        btn = QPushButton(f"  {label}")
        btn.setCheckable(True)
        btn.setFixedHeight(44)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(self._btn_style(False))
        btn.clicked.connect(lambda _, i=idx: self._select(i))
        return btn

    def _btn_style(self, active):
        if active:
            return f"""
                QPushButton {{
                    background: {SIDEBAR_SEL};
                    color: {WHITE};
                    border: none;
                    border-left: 3px solid {ACCENT};
                    text-align: left;
                    padding: 0 20px;
                    font-size: 13px;
                    font-weight: 600;
                    letter-spacing: 0.2px;
                }}
            """
        return f"""
            QPushButton {{
                background: transparent;
                color: {SIDEBAR_T};
                border: none;
                border-left: 3px solid transparent;
                text-align: left;
                padding: 0 20px;
                font-size: 13px;
                font-weight: 400;
            }}
            QPushButton:hover {{
                background: {SIDEBAR_HV};
                color: {WHITE};
            }}
        """

    def _select(self, idx):
        if idx == self._current:
            return
        self._current = idx
        for i, b in enumerate(self._buttons):
            active = (i == idx)
            b.setChecked(active)
            b.setStyleSheet(self._btn_style(active))
        self.page_changed.emit(idx)

    def select_external(self, idx):
        """Selecciona una página desde fuera (sin emitir señal de vuelta)."""
        self._select(idx)
