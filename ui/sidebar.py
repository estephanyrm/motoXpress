# ─────────────────────────────────────────────
#  MotoXpress — Sidebar (v3)
# ─────────────────────────────────────────────
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from ui.styles import (
    SIDEBAR_BG, SIDEBAR_T, SIDEBAR_A, SIDEBAR_HV, SIDEBAR_SEL, SIDEBAR_ACC,
    ACCENT, WHITE, TEXT2, FONT_FAMILY
)
from ui.widgets import make_label


class Sidebar(QWidget):
    page_changed = pyqtSignal(int)

    # (etiqueta, emoji-icon)
    ITEMS = [
        ("Dashboard",   "◈"),
        ("Motos",       "◉"),
        ("Clientes",    "◎"),
        ("Empleados",   "◆"),
        ("Nueva Venta", "◇"),
        ("Ventas",      "▣"),
        ("Categorías",  "◐"),
    ]

    def __init__(self):
        super().__init__()
        self.setFixedWidth(216)
        self.setObjectName("sidebar")
        self.setStyleSheet(f"QWidget {{ background: {SIDEBAR_BG}; border: none; }}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Logo ──
        logo_wrap = QWidget()
        logo_wrap.setFixedHeight(66)
        logo_wrap.setStyleSheet(
            f"background: {SIDEBAR_BG}; "
            f"border-bottom: 1px solid rgba(255,255,255,0.07);"
        )
        ll = QHBoxLayout(logo_wrap)
        ll.setContentsMargins(18, 0, 18, 0)
        ll.setSpacing(9)

        indicator = QLabel("●")
        indicator.setStyleSheet(f"color: {SIDEBAR_ACC}; font-size: 9px; background: transparent;")
        title_lbl = QLabel("MotoXpress")
        title_lbl.setStyleSheet(
            f"color: {WHITE}; font-size: 14px; font-weight: 700; "
            f"letter-spacing: 0.6px; background: transparent; "
            f"font-family: {FONT_FAMILY};"
        )
        ll.addWidget(indicator)
        ll.addWidget(title_lbl)
        ll.addStretch()
        layout.addWidget(logo_wrap)

        layout.addSpacing(18)

        # ── Etiqueta de grupo ──
        nav_label = QLabel("MENÚ")
        nav_label.setStyleSheet(
            f"color: rgba(156,163,175,0.50); font-size: 9px; font-weight: 700; "
            f"letter-spacing: 1.4px; background: transparent; padding: 0 18px; "
            f"font-family: {FONT_FAMILY};"
        )
        layout.addWidget(nav_label)
        layout.addSpacing(6)

        # ── Botones de navegación ──
        self._buttons = []
        for i, (label, icon) in enumerate(self.ITEMS):
            btn = self._make_btn(i, label, icon)
            layout.addWidget(btn)
            self._buttons.append(btn)

        layout.addStretch()

        # ── Footer ──
        ver = QLabel("v3.0 — MotoXpress")
        ver.setStyleSheet(
            f"color: rgba(156,163,175,0.30); font-size: 10px; "
            f"background: transparent; padding: 14px 18px; "
            f"font-family: {FONT_FAMILY};"
        )
        layout.addWidget(ver)

        self._current = -1
        self._select(0)

    def _make_btn(self, idx, label, icon):
        btn = QPushButton(f"   {label}")
        btn.setCheckable(True)
        btn.setFixedHeight(42)
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
                    border-left: 3px solid {SIDEBAR_ACC};
                    text-align: left;
                    padding: 0 18px;
                    font-size: 13px;
                    font-weight: 600;
                    letter-spacing: 0.1px;
                    font-family: {FONT_FAMILY};
                }}
            """
        return f"""
            QPushButton {{
                background: transparent;
                color: {SIDEBAR_T};
                border: none;
                border-left: 3px solid transparent;
                text-align: left;
                padding: 0 18px;
                font-size: 13px;
                font-weight: 400;
                font-family: {FONT_FAMILY};
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
        self._select(idx)
