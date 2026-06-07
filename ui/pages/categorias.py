from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QScrollArea, QLabel, QSizePolicy,
    QDialog, QFormLayout, QLineEdit, QTextEdit,
    QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt

from ui.styles import (
    STYLE_INPUT, STYLE_INPUT_ERROR,
    ACCENT, ACCENT_L, ACCENT_H,
    SUCCESS, SUCCESS_L, DANGER, DANGER_L, WARNING, WARNING_L,
    TEXT, TEXT2, TEXT3, WHITE, BORDER, BORDER2, PANEL, OFF_WHITE,
    FONT_FAMILY,
    btn_primary, btn_secondary, btn_danger, card_style
)
from ui.widgets import (
    make_label, make_divider, make_badge,
    show_error, show_ok, show_confirm, STYLE_CHECKBOX
)


#  Página principal de Categorías
class CategoriasPage(QWidget):

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self._ctrl = controller
        self._build()

    # ── Construcción de la UI ─────────────────────────────────────────────
    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(20)

        # Encabezado
        header_row = QHBoxLayout()
        hv = QVBoxLayout()
        hv.setSpacing(3)
        hv.addWidget(make_label("Categorías de Motos", size=20, bold=True))
        hv.addWidget(make_label(
            "Administra categorías y asigna tipos a las motos del inventario.",
            size=13, color=TEXT2
        ))
        header_row.addLayout(hv)
        header_row.addStretch()

        btn_nueva = QPushButton("  + Nueva categoría")
        btn_nueva.setStyleSheet(btn_primary())
        btn_nueva.setCursor(Qt.PointingHandCursor)
        btn_nueva.setFixedHeight(38)
        btn_nueva.clicked.connect(self._abrir_form_crear)
        header_row.addWidget(btn_nueva)
        root.addLayout(header_row)

        # Divisor
        root.addWidget(make_divider())

        # ── Layout de dos columnas ──
        cols = QHBoxLayout()
        cols.setSpacing(20)

        # Columna izquierda: lista de categorías
        self._left_panel = self._build_left_panel()
        cols.addWidget(self._left_panel)

        # Columna derecha: asignar categoría a moto
        # right_panel = self._build_right_panel()
        # cols.addWidget(right_panel, stretch=2)

        root.addLayout(cols)
        self._reload()

    def _build_left_panel(self):
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border: 1.5px solid {BORDER};
                border-radius: 12px;
            }}
        """)
        panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header del panel
        ph = QWidget()
        ph.setStyleSheet(f"""
            background: {PANEL};
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            border-bottom: 1.5px solid {BORDER};
        """)
        ph_layout = QHBoxLayout(ph)
        ph_layout.setContentsMargins(22, 14, 22, 14)
        ph_layout.addWidget(make_label("Categorías registradas", size=13, bold=True, color=TEXT))
        ph_layout.addStretch()
        self._count_lbl = make_label("0 categorías", size=12, color=TEXT3)
        ph_layout.addWidget(self._count_lbl)
        layout.addWidget(ph)

        # Área scrollable para las cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        self._cards_widget = QWidget()
        self._cards_widget.setStyleSheet("background: transparent;")
        self._cards_layout = QVBoxLayout(self._cards_widget)
        self._cards_layout.setContentsMargins(18, 16, 18, 16)
        self._cards_layout.setSpacing(10)

        scroll.setWidget(self._cards_widget)
        layout.addWidget(scroll)
        return panel

    def _build_right_panel(self):
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border: 1.5px solid {BORDER};
                border-radius: 12px;
            }}
        """)
        panel.setMinimumWidth(300)
        panel.setMaximumWidth(360)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header del panel
        ph = QWidget()
        ph.setStyleSheet(f"""
            background: {PANEL};
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            border-bottom: 1.5px solid {BORDER};
        """)
        ph_layout = QHBoxLayout(ph)
        ph_layout.setContentsMargins(22, 14, 22, 14)
        ph_layout.addWidget(make_label("Asignar a moto", size=13, bold=True, color=TEXT))
        layout.addWidget(ph)

        # Contenido
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        cl = QVBoxLayout(content)
        cl.setContentsMargins(22, 20, 22, 20)
        cl.setSpacing(14)

        cl.addWidget(make_label(
            "Elige una moto y marca las categorías que quieres asignarle.",
            size=12, color=TEXT2, wrap=True
        ))

        cl.addWidget(make_label("Moto:", size=12, color=TEXT2))
        self._moto_combo = QComboBox()
        self._moto_combo.setStyleSheet(STYLE_INPUT)
        self._moto_combo.currentIndexChanged.connect(self._on_moto_selected)
        cl.addWidget(self._moto_combo)

        cl.addWidget(make_divider())
        cl.addWidget(make_label("Categorías disponibles:", size=12, color=TEXT2))

        # Scroll para los checkboxes
        checks_scroll = QScrollArea()
        checks_scroll.setWidgetResizable(True)
        checks_scroll.setFrameShape(QFrame.NoFrame)
        checks_scroll.setFixedHeight(200)
        checks_scroll.setStyleSheet("background: transparent;")

        self._checks_widget = QWidget()
        self._checks_widget.setStyleSheet("background: transparent;")
        self._checks_layout = QVBoxLayout(self._checks_widget)
        self._checks_layout.setContentsMargins(0, 0, 0, 0)
        self._checks_layout.setSpacing(8)
        checks_scroll.setWidget(self._checks_widget)
        cl.addWidget(checks_scroll)

        cl.addStretch()

        btn_guardar = QPushButton("Guardar asignación")
        btn_guardar.setStyleSheet(btn_primary())
        btn_guardar.setCursor(Qt.PointingHandCursor)
        btn_guardar.setFixedHeight(38)
        btn_guardar.clicked.connect(self._guardar_asignacion)
        cl.addWidget(btn_guardar)

        layout.addWidget(content)
        return panel

    # ── Carga de datos ────────────────────────────────────────────────────
    def refresh(self):
        """Refresca la página (se llama al navegar a ella)."""
        self._reload()

    def _reload(self):
        """Recarga categorías y combo de motos."""
        self._load_cats()
        # self._load_moto_combo()

    def _load_cats(self):
        """Limpia y repopula las cards de categoría."""
        # Limpiar widgets existentes
        while self._cards_layout.count():
            item = self._cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            cats = self._ctrl.listar_categorias()
        except Exception as e:
            show_error(self, f"Error al cargar categorías: {e}")
            return

        # Actualizar contador
        n = len(cats)
        self._count_lbl.setText(f"{n} categoría{'s' if n != 1 else ''}")

        if not cats:
            empty = QWidget()
            empty.setStyleSheet("background: transparent;")
            el = QVBoxLayout(empty)
            el.setAlignment(Qt.AlignCenter)
            el.setSpacing(8)
            el.addWidget(make_label("📂", size=32), alignment=Qt.AlignCenter)
            el.addWidget(
                make_label("No hay categorías registradas.", size=13, color=TEXT3),
                alignment=Qt.AlignCenter
            )
            el.addWidget(
                make_label("Crea la primera usando el botón de arriba.", size=12, color=TEXT3, italic=True),
                alignment=Qt.AlignCenter
            )
            self._cards_layout.addWidget(empty)
        else:
            for cat in cats:
                self._cards_layout.addWidget(self._make_cat_card(cat))

        self._cards_layout.addStretch()

    def _make_cat_card(self, cat):
        """Crea una card para una categoría con botones de editar y eliminar."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: {OFF_WHITE};
                border: 1.5px solid {BORDER};
                border-radius: 10px;
            }}
            QFrame:hover {{
                border-color: {BORDER2};
                background: {WHITE};
            }}
        """)

        cl = QHBoxLayout(card)
        cl.setContentsMargins(16, 12, 16, 12)
        cl.setSpacing(12)

        # Info izquierda
        info = QVBoxLayout()
        info.setSpacing(3)
        info.addWidget(make_label(cat.nombre or "", size=13, bold=True))
        desc = cat.descripcion or "Sin descripción"
        lbl_desc = make_label(desc, size=12, color=TEXT2, wrap=True)
        lbl_desc.setMaximumWidth(300)
        info.addWidget(lbl_desc)
        cl.addLayout(info)
        cl.addStretch()

        # Badge ID
        badge = make_badge(f"#{cat.id_categoria}", color=ACCENT, bg=ACCENT_L)
        cl.addWidget(badge)

        # Botón Editar
        btn_edit = QPushButton("Editar")
        btn_edit.setFixedHeight(32)
        btn_edit.setMinimumWidth(90)
        btn_edit.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: #FFFFFF;
                border: none;
                border-radius: 7px;
                font-size: 12px;
                font-weight: 600;
                font-family: {FONT_FAMILY};
            }}
            QPushButton:hover {{
                background-color: {ACCENT_H};
            }}
        """)
        btn_edit.setCursor(Qt.PointingHandCursor)
        btn_edit.clicked.connect(lambda _, c=cat: self._abrir_form_editar(c))
        cl.addWidget(btn_edit)

        # Botón Eliminar
        btn_del = QPushButton("Eliminar")
        btn_del.setFixedHeight(32)
        btn_del.setMinimumWidth(90)
        btn_del.setStyleSheet(f"""
            QPushButton {{
                background-color: {DANGER};
                color: #FFFFFF;
                border: none;
                border-radius: 7px;
                font-size: 12px;
                font-weight: 600;
                font-family: {FONT_FAMILY};
            }}
            QPushButton:hover {{
                background-color: #7F1D1D;
            }}
        """)
        btn_del.setCursor(Qt.PointingHandCursor)
        btn_del.clicked.connect(lambda _, c=cat: self._eliminar_categoria(c))
        cl.addWidget(btn_del)

        return card

    def _load_moto_combo(self):
        """Carga el combo de motos bloqueando señales para evitar disparos espurios."""
        self._moto_combo.blockSignals(True)
        self._moto_combo.clear()
        self._moto_combo.addItem("— Seleccionar moto —", None)
        try:
            for m in self._ctrl.motos_disponibles():
                label = f"[{m.id_moto}] {m.marca} {m.modelo}"
                self._moto_combo.addItem(label, m.id_moto)
        except Exception as e:
            show_error(self, f"Error al cargar motos: {e}")
        self._moto_combo.blockSignals(False)
        self._build_checks([], set())

    def _on_moto_selected(self):
        """Se dispara cuando el usuario selecciona una moto en el combo."""
        id_moto = self._moto_combo.currentData()
        if id_moto is None:
            self._build_checks([], set())
            return
        try:
            moto = self._ctrl.detalle_moto(id_moto)
            if moto is None:
                self._build_checks([], set())
                return
            moto.cargar_categorias()
            ids_asignadas = {c.id_categoria for c in moto.categorias}
            cats = self._ctrl.listar_categorias()
            self._build_checks(cats, ids_asignadas)
        except Exception as e:
            show_error(self, f"Error al cargar datos de moto: {e}")
            self._build_checks([], set())

    def _build_checks(self, categorias, ids_asignadas: set):
        """Reconstruye la lista de checkboxes según las categorías disponibles."""
        # Limpiar
        while self._checks_layout.count():
            item = self._checks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._cat_checks = []

        if not categorias:
            self._checks_layout.addWidget(
                make_label(
                    "Selecciona una moto para ver las categorías.",
                    size=12, color=TEXT3, wrap=True
                )
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

    # ── Acciones de categorías ────────────────────────────────────────────
    def _abrir_form_crear(self):
        """Abre el diálogo para crear una nueva categoría."""
        dlg = _CategoriaDialog(self, titulo="Nueva categoría")
        if dlg.exec_() == QDialog.Accepted:
            nombre, descripcion = dlg.get_data()
            try:
                self._ctrl.crear_categoria(nombre, descripcion)
                self._reload()
                show_ok(self, f"Categoría «{nombre}» creada correctamente.")
            except Exception as e:
                show_error(self, f"No se pudo crear la categoría: {e}")

    def _abrir_form_editar(self, cat):
        """Abre el diálogo para editar una categoría existente."""
        dlg = _CategoriaDialog(
            self,
            titulo=f"Editar categoría #{cat.id_categoria}",
            nombre_inicial=cat.nombre or "",
            desc_inicial=cat.descripcion or ""
        )
        if dlg.exec_() == QDialog.Accepted:
            nombre, descripcion = dlg.get_data()
            try:
                self._ctrl.actualizar_categoria(cat.id_categoria, nombre, descripcion)
                self._reload()
                show_ok(self, f"Categoría «{nombre}» actualizada.")
            except Exception as e:
                show_error(self, f"No se pudo actualizar la categoría: {e}")

    def _eliminar_categoria(self, cat):
        """Pide confirmación y elimina la categoría."""
        if not show_confirm(
            self,
            f"¿Eliminar la categoría «{cat.nombre}»?\n\n"
            "Esta acción también quitará esta categoría de todas las motos asociadas.",
            title="Confirmar eliminación"
        ):
            return
        try:
            self._ctrl.eliminar_categoria(cat.id_categoria)
            self._reload()
        except Exception as e:
            show_error(self, f"No se pudo eliminar la categoría: {e}")

    # ── Asignación de categorías a motos ──────────────────────────────────
    def _guardar_asignacion(self):
        """
        Guarda la asignación de categorías a la moto seleccionada.
        Actualiza las categorías embebidas directamente en MongoDB.
        """
        id_moto = self._moto_combo.currentData()
        if id_moto is None:
            show_error(self, "Selecciona una moto antes de guardar.")
            return

        if not hasattr(self, '_cat_checks') or not self._cat_checks:
            show_error(self, "No hay categorías disponibles para asignar.")
            return

        try:
            moto = self._ctrl.detalle_moto(id_moto)
            if moto is None:
                show_error(self, "La moto seleccionada no existe.")
                return

            ids_nuevas = [id_cat for cb, id_cat in self._cat_checks if cb.isChecked()]
            self._ctrl.actualizar_categorias_moto(id_moto, ids_nuevas)

            # Refrescar los checks para mostrar estado actualizado
            self._on_moto_selected()
            show_ok(self, "Categorías de la moto actualizadas correctamente.")

        except Exception as e:
            show_error(self, f"Error al guardar asignación: {e}")


# ─────────────────────────────────────────────
#  Diálogo para crear/editar una categoría
# ─────────────────────────────────────────────
class _CategoriaDialog(QDialog):

    def __init__(self, parent, titulo="Categoría",
                 nombre_inicial="", desc_inicial=""):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.setMinimumWidth(420)
        self.setMaximumWidth(480)
        self.setStyleSheet(f"QDialog {{ background: {WHITE}; }}")
        self._build(titulo, nombre_inicial, desc_inicial)

    def _build(self, titulo, nombre_inicial, desc_inicial):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        layout.addWidget(make_label(titulo, size=16, bold=True))
        layout.addWidget(make_divider())

        # Nombre
        layout.addWidget(make_label("Nombre *", size=12, color=TEXT2))
        self._nombre = QLineEdit(nombre_inicial)
        self._nombre.setPlaceholderText("ej. Deportiva, Trail, Scooter…")
        self._nombre.setStyleSheet(STYLE_INPUT)
        layout.addWidget(self._nombre)

        self._err_nombre = make_label("", size=11, color=DANGER)
        self._err_nombre.setVisible(False)
        layout.addWidget(self._err_nombre)

        # Descripción
        layout.addWidget(make_label("Descripción (opcional)", size=12, color=TEXT2))
        self._desc = QTextEdit(desc_inicial)
        self._desc.setPlaceholderText("Describe brevemente esta categoría…")
        self._desc.setFixedHeight(80)
        self._desc.setStyleSheet(f"""
            QTextEdit {{
                background: {WHITE};
                border: 1.5px solid {BORDER};
                border-radius: 8px;
                padding: 8px 12px;
                color: {TEXT};
                font-size: 13px;
                font-family: {FONT_FAMILY};
            }}
            QTextEdit:focus {{
                border-color: {ACCENT};
            }}
        """)
        layout.addWidget(self._desc)

        layout.addStretch()

        # Botones
        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(btn_secondary())
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_cancel)
        btn_row.addStretch()

        btn_save = QPushButton("Guardar")
        btn_save.setStyleSheet(btn_primary())
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self._validate_and_accept)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _validate_and_accept(self):
        nombre = self._nombre.text().strip()
        if not nombre:
            self._err_nombre.setText("El nombre de la categoría es obligatorio.")
            self._err_nombre.setVisible(True)
            self._nombre.setStyleSheet(STYLE_INPUT_ERROR)
            return
        if len(nombre) < 2:
            self._err_nombre.setText("El nombre debe tener al menos 2 caracteres.")
            self._err_nombre.setVisible(True)
            self._nombre.setStyleSheet(STYLE_INPUT_ERROR)
            return
        # Limpiar error y aceptar
        self._err_nombre.setVisible(False)
        self._nombre.setStyleSheet(STYLE_INPUT)
        self.accept()

    def get_data(self):
        """Retorna (nombre, descripcion) ya limpios."""
        nombre = self._nombre.text().strip().title()
        descripcion = self._desc.toPlainText().strip() or None
        return nombre, descripcion