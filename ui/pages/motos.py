# ─────────────────────────────────────────────
#  MotoXpress — Página de Motos (v3)
#  Cambios clave:
#  1. Filtros corregidos: búsqueda + categoría combinadas sin perder estado
#  2. Carga lazy de categorías solo al inicio (_reload), no en cada filtro
#  3. Contador de resultados visible
#  4. Botón para limpiar filtros
#  5. Diálogo de registro mejorado con validaciones
# ─────────────────────────────────────────────
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame,
    QPushButton, QLineEdit, QComboBox, QDialog, QFormLayout,
    QSpinBox, QDoubleSpinBox, QLabel, QCheckBox,
    QGridLayout, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor

from ui.styles import (
    STYLE_TABLE, STYLE_INPUT, STYLE_INPUT_ERROR,
    ACCENT, ACCENT_L, SUCCESS, WARNING, DANGER,
    TEXT, TEXT2, TEXT3, WHITE, BORDER, BORDER2, PANEL, OFF_WHITE,
    STYLE_CHECKBOX, FONT_FAMILY,
    btn_primary, btn_secondary, btn_danger, card_style
)
from ui.widgets import (
    make_label, make_divider, make_badge, make_status_badge,
    show_error, show_ok, mark_invalid
)


class MotosPage(QWidget):

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self._ctrl = controller
        self._all_motos = []          # cache de motos (con categorías ya cargadas)

        # Debounce timer para la búsqueda de texto
        self._search_timer = QTimer(self)
        self._search_timer.setSingleShot(True)
        self._search_timer.setInterval(200)      # ms de espera tras última tecla
        self._search_timer.timeout.connect(self._apply_filters)

        self._build()

    # ── Construcción de la UI ─────────────────────────────────────────────
    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        # Encabezado
        header = QHBoxLayout()
        header.setSpacing(12)
        hv = QVBoxLayout()
        hv.setSpacing(3)
        hv.addWidget(make_label("Inventario de Motos", size=20, bold=True))
        hv.addWidget(make_label("Todas las motos disponibles en el sistema.", size=13, color=TEXT2))
        header.addLayout(hv)
        header.addStretch()

        # Barra de búsqueda con debounce
        self._search = QLineEdit()
        self._search.setPlaceholderText("Buscar por marca, modelo o VIN…")
        self._search.setFixedWidth(240)
        self._search.setStyleSheet(STYLE_INPUT)
        # Debounce: reinicia el timer en cada pulsación de tecla
        self._search.textChanged.connect(lambda _: self._search_timer.start())
        header.addWidget(self._search)

        # Filtro por categoría
        self._combo_cat = QComboBox()
        self._combo_cat.setFixedWidth(170)
        self._combo_cat.setStyleSheet(STYLE_INPUT)
        self._combo_cat.currentIndexChanged.connect(self._apply_filters)
        header.addWidget(self._combo_cat)

        # Botón limpiar filtros
        self._btn_clear = QPushButton("✕ Limpiar")
        self._btn_clear.setStyleSheet(btn_secondary())
        self._btn_clear.setCursor(Qt.PointingHandCursor)
        self._btn_clear.setFixedHeight(36)
        self._btn_clear.setVisible(False)   # solo visible cuando hay filtros activos
        self._btn_clear.clicked.connect(self._clear_filters)
        header.addWidget(self._btn_clear)

        # Botón registrar
        btn_reg = QPushButton("  + Registrar moto")
        btn_reg.setStyleSheet(btn_primary())
        btn_reg.setCursor(Qt.PointingHandCursor)
        btn_reg.setFixedHeight(38)
        btn_reg.clicked.connect(self._form_registrar)
        header.addWidget(btn_reg)

        layout.addLayout(header)

        # Contador de resultados
        self._results_lbl = make_label("", size=12, color=TEXT3)
        layout.addWidget(self._results_lbl)

        # Tabla
        cols = ["ID", "VIN", "Marca", "Modelo", "Año", "Color", "Precio", "Categorías", "Estado"]
        self._tbl = QTableWidget(0, len(cols))
        self._tbl.setStyleSheet(STYLE_TABLE)
        self._tbl.setHorizontalHeaderLabels(cols)
        hh = self._tbl.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.Stretch)
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        self._tbl.setFocusPolicy(Qt.NoFocus)
        self._tbl.setAlternatingRowColors(True)
        layout.addWidget(self._tbl)

        self._reload()

    # ── Carga de datos ────────────────────────────────────────────────────
    def refresh(self):
        """Punto de entrada cuando el usuario navega a esta página."""
        self._reload()

    def _reload(self):
        """
        Carga TODAS las motos con sus categorías pre-hidratadas y
        reconstruye el combo de filtros.
        El filtrado NO toca la BD — opera solo sobre _all_motos.
        """
        try:
            # Las categorías ya vienen cargadas (eager) desde MotoDAO.listar_disponibles
            motos = self._ctrl.motos_disponibles()
            self._all_motos = motos
        except Exception as e:
            show_error(self, f"Error al cargar motos: {e}")
            self._all_motos = []

        self._load_categorias_combo()
        self._apply_filters()

    def _load_categorias_combo(self):
        """Repopula el combo de filtro por categoría sin disparar filtros."""
        self._combo_cat.blockSignals(True)
        prev_data = self._combo_cat.currentData()   # recordar selección previa
        self._combo_cat.clear()
        self._combo_cat.addItem("Todas las categorías", None)
        try:
            cats = self._ctrl.listar_categorias()
            for c in cats:
                self._combo_cat.addItem(c.nombre, c.id_categoria)
        except Exception:
            pass
        # Restaurar selección previa si todavía existe
        restored = False
        if prev_data is not None:
            for i in range(self._combo_cat.count()):
                if self._combo_cat.itemData(i) == prev_data:
                    self._combo_cat.setCurrentIndex(i)
                    restored = True
                    break
        if not restored:
            self._combo_cat.setCurrentIndex(0)
        self._combo_cat.blockSignals(False)

    # ── Lógica de filtrado ────────────────────────────────────────────────
    def _apply_filters(self):
        """
        Filtra _all_motos en memoria combinando texto de búsqueda y
        categoría. No toca la BD.
        """
        text   = self._search.text().lower().strip()
        cat_id = self._combo_cat.currentData()       # None = todas

        result = self._all_motos

        # Filtro de texto (marca, modelo, vin)
        if text:
            result = [
                m for m in result
                if text in (m.marca  or "").lower()
                or text in (m.modelo or "").lower()
                or text in (m.vin    or "").lower()
            ]

        # Filtro por categoría
        if cat_id is not None:
            result = [
                m for m in result
                if any(c.id_categoria == cat_id for c in (m.categorias or []))
            ]

        # Mostrar / ocultar botón de limpiar
        has_filters = bool(text) or cat_id is not None
        self._btn_clear.setVisible(has_filters)

        self._populate(result)

    def _clear_filters(self):
        """Limpia todos los filtros y muestra todas las motos."""
        self._search.blockSignals(True)
        self._search.clear()
        self._search.blockSignals(False)
        self._combo_cat.blockSignals(True)
        self._combo_cat.setCurrentIndex(0)
        self._combo_cat.blockSignals(False)
        self._btn_clear.setVisible(False)
        self._populate(self._all_motos)

    # ── Renderizado de tabla ──────────────────────────────────────────────
    def _populate(self, motos):
        """Llena la tabla con la lista filtrada de motos."""
        color_map = {
            "disponible": SUCCESS,
            "vendida":    DANGER,
            "reservada":  WARNING,
        }
        self._tbl.setRowCount(len(motos))

        for i, m in enumerate(motos):
            def cell(val, align=Qt.AlignVCenter | Qt.AlignLeft):
                item = QTableWidgetItem(val)
                item.setTextAlignment(align)
                return item

            self._tbl.setItem(i, 0, cell(str(m.id_moto)))
            self._tbl.setItem(i, 1, cell(m.vin or "—"))
            self._tbl.setItem(i, 2, cell(m.marca or "—"))
            self._tbl.setItem(i, 3, cell(m.modelo or "—"))
            self._tbl.setItem(i, 4, cell(str(m.anio or "—")))
            self._tbl.setItem(i, 5, cell(m.color or "—"))

            precio_item = QTableWidgetItem(
                f"${m.precio:,.0f}" if m.precio is not None else "—"
            )
            precio_item.setForeground(QColor(SUCCESS))
            self._tbl.setItem(i, 6, precio_item)

            cats_txt = (
                ", ".join(c.nombre for c in m.categorias)
                if m.categorias else "Sin categoría"
            )
            cat_item = QTableWidgetItem(cats_txt)
            cat_item.setForeground(QColor(ACCENT if m.categorias else TEXT3))
            self._tbl.setItem(i, 7, cat_item)

            estado_item = QTableWidgetItem((m.estado or "").capitalize())
            estado_item.setForeground(QColor(color_map.get(m.estado or "", TEXT2)))
            self._tbl.setItem(i, 8, estado_item)

        self._tbl.resizeRowsToContents()

        # Actualizar contador de resultados
        total = len(self._all_motos)
        shown = len(motos)
        if shown == total:
            self._results_lbl.setText(f"{total} moto{'s' if total != 1 else ''} en inventario")
        else:
            self._results_lbl.setText(
                f"Mostrando {shown} de {total} motos"
            )

    # ── Diálogo de registro ───────────────────────────────────────────────
    def _form_registrar(self):
        try:
            cats = self._ctrl.listar_categorias()
        except Exception as e:
            show_error(self, str(e))
            cats = []

        dialog = _MotoDialog(self, self._ctrl, cats)
        if dialog.exec_() == QDialog.Accepted:
            self._reload()


# ─────────────────────────────────────────────
#  Diálogo: Registrar moto
# ─────────────────────────────────────────────
class _MotoDialog(QDialog):

    def __init__(self, parent, controller, categorias):
        super().__init__(parent)
        self._ctrl = controller
        self._categorias = categorias
        self.setWindowTitle("Registrar nueva moto")
        self.setMinimumWidth(500)
        self.setMaximumWidth(580)
        self.setStyleSheet(f"QDialog {{ background: {WHITE}; }}")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(18)

        layout.addWidget(make_label("Nueva moto", size=17, bold=True))
        layout.addWidget(make_label(
            "Los campos marcados con * son obligatorios.",
            size=12, color=TEXT2
        ))
        layout.addWidget(make_divider())

        # ── Formulario ──
        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        def txt(placeholder=""):
            w = QLineEdit()
            w.setPlaceholderText(placeholder)
            w.setStyleSheet(STYLE_INPUT)
            return w

        def row_with_err(label_txt, widget):
            """Agrega un campo con su etiqueta de error debajo."""
            container = QWidget()
            container.setStyleSheet("background: transparent; border: none;")
            vl = QVBoxLayout(container)
            vl.setContentsMargins(0, 0, 0, 0)
            vl.setSpacing(3)
            vl.addWidget(widget)
            err = make_label("", size=11, color=DANGER)
            err.setVisible(False)
            vl.addWidget(err)
            form.addRow(make_label(label_txt, size=12, color=TEXT2), container)
            return err

        self._vin    = txt("ej. 1HGBH41JXMN109186")
        self._marca  = txt("ej. Honda")
        self._modelo = txt("ej. CB500F")
        self._color  = txt("ej. Rojo")

        self._anio = QSpinBox()
        self._anio.setRange(1980, 2030)
        self._anio.setValue(2024)
        self._anio.setStyleSheet(STYLE_INPUT)

        self._precio = QDoubleSpinBox()
        self._precio.setRange(0, 999_999_999)
        self._precio.setDecimals(0)
        self._precio.setPrefix("$")
        self._precio.setSingleStep(100_000)
        self._precio.setStyleSheet(STYLE_INPUT)

        self._estado_combo = QComboBox()
        self._estado_combo.addItems(["disponible", "reservada"])
        self._estado_combo.setStyleSheet(STYLE_INPUT)

        self._err_vin    = row_with_err("VIN *",    self._vin)
        self._err_marca  = row_with_err("Marca *",  self._marca)
        self._err_modelo = row_with_err("Modelo *", self._modelo)
        row_with_err("Año *",    self._anio)
        self._err_precio = row_with_err("Precio *", self._precio)
        row_with_err("Color",    self._color)
        row_with_err("Estado",   self._estado_combo)

        layout.addLayout(form)

        # ── Sección categorías ──
        layout.addWidget(make_label("Categorías", size=13, bold=True))
        layout.addWidget(make_label(
            "Selecciona una o más categorías para esta moto.", size=12, color=TEXT2
        ))

        if self._categorias:
            cat_frame = QFrame()
            cat_frame.setStyleSheet(f"""
                QFrame {{
                    background: {PANEL};
                    border: 1.5px solid {BORDER};
                    border-radius: 8px;
                }}
            """)
            cat_layout = QGridLayout(cat_frame)
            cat_layout.setContentsMargins(16, 14, 16, 14)
            cat_layout.setSpacing(10)

            self._cat_checks = []
            for idx, cat in enumerate(self._categorias):
                cb = QCheckBox(cat.nombre)
                cb.setToolTip(cat.descripcion or "")
                cb.setStyleSheet(STYLE_CHECKBOX)
                row, col = divmod(idx, 3)
                cat_layout.addWidget(cb, row, col)
                self._cat_checks.append((cb, cat.id_categoria))

            layout.addWidget(cat_frame)
        else:
            self._cat_checks = []
            layout.addWidget(make_label(
                "No hay categorías disponibles.", size=12, color=TEXT3, italic=True
            ))

        # ── Botones ──
        layout.addStretch()
        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(btn_secondary())
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_cancel)
        btn_row.addStretch()

        btn_save = QPushButton("  Registrar moto")
        btn_save.setStyleSheet(btn_primary())
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self._save)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    # ── Validación ────────────────────────────────────────────────────────
    def _validate(self):
        ok = True

        def check(widget, err_lbl, condition, msg):
            nonlocal ok
            if not condition:
                widget.setStyleSheet(STYLE_INPUT_ERROR)
                err_lbl.setText(msg)
                err_lbl.setVisible(True)
                ok = False
            else:
                widget.setStyleSheet(STYLE_INPUT)
                err_lbl.setVisible(False)

        check(self._vin, self._err_vin,
              len(self._vin.text().strip()) >= 3,
              "El VIN es obligatorio (mín. 3 caracteres).")
        check(self._marca, self._err_marca,
              len(self._marca.text().strip()) >= 2,
              "La marca es obligatoria.")
        check(self._modelo, self._err_modelo,
              len(self._modelo.text().strip()) >= 1,
              "El modelo es obligatorio.")
        check(self._precio, self._err_precio,
              self._precio.value() > 0,
              "El precio debe ser mayor a $0.")
        return ok

    def _save(self):
        from model.VO.MotoVO import MotoVO
        if not self._validate():
            return

        ids_categorias = [
            id_cat for cb, id_cat in self._cat_checks if cb.isChecked()
        ]

        try:
            moto = MotoVO(
                id_moto=0,
                vin=self._vin.text().strip().upper(),
                marca=self._marca.text().strip().title(),
                modelo=self._modelo.text().strip(),
                anio=self._anio.value(),
                precio=self._precio.value(),
                color=self._color.text().strip().title() or None,
                estado=self._estado_combo.currentText(),
            )
            id_nuevo = self._ctrl.registrar_moto(moto, ids_categorias or None)
            show_ok(self, f"Moto registrada con ID #{id_nuevo}.")
            self.accept()
        except Exception as e:
            show_error(self, str(e))