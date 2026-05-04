# ─────────────────────────────────────────────
#  MotoXpress — Página de Motos
# ─────────────────────────────────────────────
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame, QScrollArea,
    QPushButton, QLineEdit, QComboBox, QDialog, QFormLayout,
    QSpinBox, QDoubleSpinBox, QLabel, QCheckBox, QGroupBox,
    QGridLayout, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

from ui.styles import (
    STYLE_TABLE, STYLE_INPUT, STYLE_INPUT_ERROR,
    ACCENT, SUCCESS, WARNING, DANGER, TEXT, TEXT2, TEXT3,
    WHITE, BORDER, PANEL, OFF_WHITE, STYLE_CHECKBOX,
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
        self._all_motos = []
        self._cat_filter = None   # id_categoria actual o None
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
        hv.addWidget(make_label("Inventario de Motos", size=20, bold=True))
        hv.addWidget(make_label("Todas las motos disponibles en el sistema", size=13, color=TEXT2))
        header.addLayout(hv)
        header.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("Buscar por marca, modelo o VIN…")
        self._search.setFixedWidth(260)
        self._search.setStyleSheet(STYLE_INPUT)
        self._search.textChanged.connect(self._apply_filters)
        header.addWidget(self._search)

        self._combo_cat = QComboBox()
        self._combo_cat.setFixedWidth(180)
        self._combo_cat.setStyleSheet(STYLE_INPUT)
        self._combo_cat.currentIndexChanged.connect(self._apply_filters)
        header.addWidget(self._combo_cat)

        btn_reg = QPushButton("  + Registrar moto")
        btn_reg.setStyleSheet(btn_primary())
        btn_reg.setCursor(Qt.PointingHandCursor)
        btn_reg.setFixedHeight(38)
        btn_reg.clicked.connect(self._form_registrar)
        header.addWidget(btn_reg)

        layout.addLayout(header)

        # ── Tabla ──
        cols = ["ID", "VIN", "Marca", "Modelo", "Año", "Color", "Precio", "Categorías", "Estado"]
        self._tbl = QTableWidget(0, len(cols))
        self._tbl.setStyleSheet(STYLE_TABLE)
        self._tbl.setHorizontalHeaderLabels(cols)
        hh = self._tbl.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.Stretch)
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        self._tbl.setFocusPolicy(Qt.NoFocus)
        self._tbl.setAlternatingRowColors(True)
        layout.addWidget(self._tbl)

        self._reload()

    def _load_categorias_combo(self):
        self._combo_cat.blockSignals(True)
        self._combo_cat.clear()
        self._combo_cat.addItem("Todas las categorías", None)
        try:
            cats = self._ctrl.listar_categorias()
            for c in cats:
                self._combo_cat.addItem(c.nombre, c.id_categoria)
        except Exception:
            pass
        self._combo_cat.blockSignals(False)

    def _reload(self):
        try:
            self._all_motos = self._ctrl.motos_disponibles()
            # Carga categorías de cada moto
            for m in self._all_motos:
                try:
                    m.cargar_categorias()
                except Exception:
                    pass
        except Exception as e:
            show_error(self, str(e))
            self._all_motos = []
        self._load_categorias_combo()
        self._apply_filters()

    def _apply_filters(self):
        text = self._search.text().lower().strip()
        cat_id = self._combo_cat.currentData()

        result = self._all_motos

        if text:
            result = [
                m for m in result
                if text in (m.marca or "").lower()
                or text in (m.modelo or "").lower()
                or text in (m.vin or "").lower()
            ]

        if cat_id is not None:
            result = [
                m for m in result
                if any(c.id_categoria == cat_id for c in m.categorias)
            ]

        self._populate(result)

    def _populate(self, motos):
        self._tbl.setRowCount(len(motos))
        color_map = {"disponible": SUCCESS, "vendida": DANGER, "reservada": WARNING}

        for i, m in enumerate(motos):
            self._tbl.setItem(i, 0, QTableWidgetItem(str(m.id_moto)))
            self._tbl.setItem(i, 1, QTableWidgetItem(m.vin or ""))
            self._tbl.setItem(i, 2, QTableWidgetItem(m.marca or ""))
            self._tbl.setItem(i, 3, QTableWidgetItem(m.modelo or ""))
            self._tbl.setItem(i, 4, QTableWidgetItem(str(m.anio or "")))
            self._tbl.setItem(i, 5, QTableWidgetItem(m.color or ""))

            precio_item = QTableWidgetItem(
                f"${m.precio:,.0f}" if m.precio is not None else "—"
            )
            precio_item.setForeground(QColor(SUCCESS))
            self._tbl.setItem(i, 6, precio_item)

            cats_txt = ", ".join(c.nombre for c in m.categorias) if m.categorias else "Sin categoría"
            cat_item = QTableWidgetItem(cats_txt)
            cat_item.setForeground(QColor(ACCENT if m.categorias else TEXT3))
            self._tbl.setItem(i, 7, cat_item)

            estado_item = QTableWidgetItem((m.estado or "").capitalize())
            estado_item.setForeground(QColor(color_map.get(m.estado or "", TEXT2)))
            self._tbl.setItem(i, 8, estado_item)

        self._tbl.resizeRowsToContents()

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
        self.setStyleSheet(f"QDialog {{ background: {WHITE}; }}")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        layout.addWidget(make_label("Nueva moto", size=17, bold=True))
        layout.addWidget(make_label(
            "Todos los campos con * son obligatorios.", size=12, color=TEXT2
        ))
        layout.addWidget(make_divider())

        # ── Campos del formulario ──
        form = QFormLayout()
        form.setSpacing(14)
        form.setLabelAlignment(Qt.AlignRight)
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        def field(placeholder=""):
            w = QLineEdit()
            w.setPlaceholderText(placeholder)
            w.setStyleSheet(STYLE_INPUT)
            return w

        self._vin    = field("ej. 1HGBH41JXMN109186")
        self._marca  = field("ej. Honda")
        self._modelo = field("ej. CB500F")
        self._color  = field("ej. Rojo")

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

        # Campos con etiquetas de error
        def field_row(lbl, widget, err_text=""):
            container = QWidget()
            container.setStyleSheet("background: transparent; border: none;")
            vl = QVBoxLayout(container)
            vl.setContentsMargins(0, 0, 0, 0)
            vl.setSpacing(3)
            vl.addWidget(widget)
            err = make_label("", size=11, color=DANGER)
            err.setVisible(False)
            vl.addWidget(err)
            form.addRow(make_label(lbl, size=13, color=TEXT2), container)
            return err

        self._err_vin    = field_row("VIN *",    self._vin)
        self._err_marca  = field_row("Marca *",  self._marca)
        self._err_modelo = field_row("Modelo *", self._modelo)
        field_row("Año *",    self._anio)
        self._err_precio = field_row("Precio *", self._precio)
        field_row("Color",    self._color)
        field_row("Estado",   self._estado_combo)

        layout.addLayout(form)

        # ── Sección categorías ──
        layout.addWidget(make_label("Categorías", size=13, bold=True))
        layout.addWidget(make_label(
            "Selecciona una o más categorías para esta moto.", size=12, color=TEXT2
        ))

        if self._categorias:
            cat_frame = QFrame()
            cat_frame.setStyleSheet(f"""
                QFrame {{ background: {PANEL}; border: 1.5px solid {BORDER}; border-radius: 8px; }}
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
        layout.addSpacing(8)
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
              bool(self._vin.text().strip()),
              "El VIN es obligatorio.")
        check(self._marca, self._err_marca,
              bool(self._marca.text().strip()),
              "La marca es obligatoria.")
        check(self._modelo, self._err_modelo,
              bool(self._modelo.text().strip()),
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
            id_nuevo = self._ctrl.registrar_moto(moto, ids_categorias if ids_categorias else None)
            show_ok(self, f"Moto registrada con ID #{id_nuevo}.")
            self.accept()
        except Exception as e:
            show_error(self, str(e))
