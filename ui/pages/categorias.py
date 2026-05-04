# ─────────────────────────────────────────────
#  MotoXpress — Página de Categorías
# ─────────────────────────────────────────────
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QComboBox, QLabel,
    QSplitter, QCheckBox, QGridLayout, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

from ui.styles import (
    STYLE_TABLE, STYLE_INPUT, STYLE_CHECKBOX,
    ACCENT, ACCENT_L, SUCCESS, SUCCESS_L, TEXT, TEXT2, TEXT3,
    WHITE, BORDER, PANEL, OFF_WHITE,
    btn_primary, btn_secondary, card_style
)
from ui.widgets import make_label, make_divider, make_badge, show_error, show_ok


class CategoriasPage(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        layout.addWidget(make_label("Categorías de Motos", size=20, bold=True))
        layout.addWidget(make_label(
            "Consulta las categorías disponibles y asigna categorías a motos.",
            size=13, color=TEXT2
        ))

        # ── Dos paneles lado a lado ──
        split_row = QHBoxLayout()
        split_row.setSpacing(20)

        # Panel izquierdo: lista de categorías
        left = QFrame()
        left.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border: 1.5px solid {BORDER};
                border-radius: 10px;
            }}
        """)
        left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(24, 20, 24, 20)
        left_layout.setSpacing(16)
        left_layout.addWidget(make_label("Categorías registradas", size=14, bold=True))

        self._cat_container = QVBoxLayout()
        self._cat_container.setSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        scroll_content.setLayout(self._cat_container)
        scroll.setWidget(scroll_content)
        left_layout.addWidget(scroll)

        split_row.addWidget(left, stretch=1)

        # Panel derecho: asignar categoría a moto
        right = QFrame()
        right.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border: 1.5px solid {BORDER};
                border-radius: 10px;
            }}
        """)
        right.setFixedWidth(340)
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(24, 20, 24, 20)
        right_layout.setSpacing(16)

        right_layout.addWidget(make_label("Asignar categoría a moto", size=14, bold=True))
        right_layout.addWidget(make_label(
            "Selecciona una moto y marca las categorías que quieres asignarle.",
            size=12, color=TEXT2, wrap=True
        ))
        right_layout.addWidget(make_divider())

        right_layout.addWidget(make_label("Moto:", size=13, color=TEXT2))
        self._moto_combo = QComboBox()
        self._moto_combo.setStyleSheet(STYLE_INPUT)
        self._moto_combo.currentIndexChanged.connect(self._on_moto_selected)
        right_layout.addWidget(self._moto_combo)

        right_layout.addSpacing(8)
        right_layout.addWidget(make_label("Categorías:", size=13, color=TEXT2))

        self._checks_container = QWidget()
        self._checks_container.setStyleSheet("background: transparent; border: none;")
        self._checks_layout = QVBoxLayout(self._checks_container)
        self._checks_layout.setContentsMargins(0, 0, 0, 0)
        self._checks_layout.setSpacing(8)
        right_layout.addWidget(self._checks_container)

        right_layout.addStretch()

        btn_asignar = QPushButton("  Guardar asignación")
        btn_asignar.setStyleSheet(btn_primary())
        btn_asignar.setCursor(Qt.PointingHandCursor)
        btn_asignar.clicked.connect(self._asignar_categorias)
        right_layout.addWidget(btn_asignar)

        split_row.addWidget(right, stretch=0)

        layout.addLayout(split_row)

        self._reload()

    def _reload(self):
        self._load_cats()
        self._load_moto_combo()

    def _load_cats(self):
        # Limpiar
        while self._cat_container.count():
            item = self._cat_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            cats = self._ctrl.listar_categorias()
        except Exception as e:
            show_error(self, str(e))
            return

        if not cats:
            self._cat_container.addWidget(
                make_label("No hay categorías registradas.", size=13, color=TEXT3)
            )
            return

        for cat in cats:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: {OFF_WHITE};
                    border: 1.5px solid {BORDER};
                    border-radius: 8px;
                }}
            """)
            cl = QHBoxLayout(card)
            cl.setContentsMargins(18, 14, 18, 14)
            cl.setSpacing(14)

            left_v = QVBoxLayout()
            left_v.setSpacing(3)
            left_v.addWidget(make_label(cat.nombre or "", size=14, bold=True))
            left_v.addWidget(make_label(
                cat.descripcion or "Sin descripción",
                size=12, color=TEXT2, wrap=True
            ))
            cl.addLayout(left_v)
            cl.addStretch()

            badge = make_badge(f"ID #{cat.id_categoria}", color=ACCENT, bg=ACCENT_L)
            cl.addWidget(badge)
            self._cat_container.addWidget(card)

        self._cat_container.addStretch()

    def _load_moto_combo(self):
        self._moto_combo.blockSignals(True)
        self._moto_combo.clear()
        self._moto_combo.addItem("— Seleccionar moto —", None)
        try:
            for m in self._ctrl.motos_disponibles():
                label = f"[{m.id_moto}] {m.marca} {m.modelo}"
                self._moto_combo.addItem(label, m.id_moto)
        except Exception as e:
            show_error(self, str(e))
        self._moto_combo.blockSignals(False)
        self._build_checks([], [])

    def _on_moto_selected(self):
        id_moto = self._moto_combo.currentData()
        if id_moto is None:
            self._build_checks([], [])
            return
        try:
            moto = self._ctrl.detalle_moto(id_moto)
            if moto is None:
                return
            moto.cargar_categorias()
            ids_asignadas = {c.id_categoria for c in moto.categorias}
            cats = self._ctrl.listar_categorias()
            self._build_checks(cats, ids_asignadas)
        except Exception as e:
            show_error(self, str(e))

    def _build_checks(self, categorias, ids_asignadas):
        # Limpiar checks anteriores
        while self._checks_layout.count():
            item = self._checks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._cat_checks = []
        if not categorias:
            self._checks_layout.addWidget(
                make_label("Selecciona una moto primero.", size=12, color=TEXT3)
            )
            return

        for cat in categorias:
            cb = QCheckBox(cat.nombre)
            cb.setChecked(cat.id_categoria in ids_asignadas)
            cb.setStyleSheet(STYLE_CHECKBOX)
            if cat.descripcion:
                cb.setToolTip(cat.descripcion)
            self._checks_layout.addWidget(cb)
            self._cat_checks.append((cb, cat.id_categoria))

    def _asignar_categorias(self):
        from model.DAO.MotoCategoriaDAO import MotoCategoriaDAO
        from db.gestor_conexiones import connection_factory

        id_moto = self._moto_combo.currentData()
        if id_moto is None:
            show_error(self, "Selecciona una moto primero.")
            return

        if not self._cat_checks:
            show_error(self, "No hay categorías disponibles.")
            return

        try:
            moto = self._ctrl.detalle_moto(id_moto)
            moto.cargar_categorias()
            ids_actuales = {c.id_categoria for c in moto.categorias}
            ids_nuevas   = {id_cat for cb, id_cat in self._cat_checks if cb.isChecked()}

            agregar  = ids_nuevas - ids_actuales
            quitar   = ids_actuales - ids_nuevas

            with connection_factory() as conn:
                for id_cat in agregar:
                    MotoCategoriaDAO.asignar(conn, id_moto, id_cat)
                for id_cat in quitar:
                    MotoCategoriaDAO.remover(conn, id_moto, id_cat)

            show_ok(self, "Categorías actualizadas correctamente.")
            self._on_moto_selected()  # Refresh checks
        except Exception as e:
            show_error(self, str(e))
