# ─────────────────────────────────────────────
#  MotoXpress — Página Nueva Venta
# ─────────────────────────────────────────────
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QFrame, QScrollArea, QFormLayout, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal

from ui.styles import (
    STYLE_INPUT, STYLE_INPUT_ERROR,
    ACCENT, ACCENT_L, SUCCESS, DANGER, WARNING, TEXT, TEXT2, TEXT3,
    WHITE, BORDER, PANEL, OFF_WHITE,
    btn_primary, btn_secondary, btn_danger, card_style
)
from ui.widgets import make_label, make_divider, show_error, show_ok


class NuevaVentaPage(QWidget):
    venta_registrada = pyqtSignal()

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self._ctrl = controller
        self._build()

    def _build(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        scroll.setWidget(container)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(24)

        # Header
        layout.addWidget(make_label("Registrar Venta", size=20, bold=True))
        layout.addWidget(make_label(
            "Complete los datos de la transacción. Los campos con * son obligatorios.",
            size=13, color=TEXT2
        ))

        # ── Card principal ──
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border: 1.5px solid {BORDER};
                border-radius: 10px;
            }}
        """)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(32, 28, 32, 28)
        cl.setSpacing(20)

        form = QFormLayout()
        form.setSpacing(16)
        form.setLabelAlignment(Qt.AlignRight)
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # ── Cliente (combo) ──
        self._cliente_combo = QComboBox()
        self._cliente_combo.setStyleSheet(STYLE_INPUT)
        self._err_cliente = make_label("", size=11, color=DANGER)
        self._err_cliente.setVisible(False)
        self._add_form_row(form, "Cliente *", self._cliente_combo, self._err_cliente)

        # ── Moto (combo) ──
        self._moto_combo = QComboBox()
        self._moto_combo.setStyleSheet(STYLE_INPUT)
        self._err_moto = make_label("", size=11, color=DANGER)
        self._err_moto.setVisible(False)
        self._add_form_row(form, "Moto disponible *", self._moto_combo, self._err_moto)

        # ── Empleado (combo) ──
        self._empleado_combo = QComboBox()
        self._empleado_combo.setStyleSheet(STYLE_INPUT)
        self._err_empleado = make_label("", size=11, color=DANGER)
        self._err_empleado.setVisible(False)
        self._add_form_row(form, "Empleado vendedor *", self._empleado_combo, self._err_empleado)

        # ── Precio final ──
        self._precio = QDoubleSpinBox()
        self._precio.setRange(0, 999_999_999)
        self._precio.setDecimals(0)
        self._precio.setPrefix("$ ")
        self._precio.setSingleStep(100_000)
        self._precio.setStyleSheet(STYLE_INPUT)
        self._err_precio = make_label("", size=11, color=DANGER)
        self._err_precio.setVisible(False)
        self._add_form_row(form, "Precio final *", self._precio, self._err_precio)

        # ── Tipo de pago ──
        self._tipo_pago = QComboBox()
        self._tipo_pago.addItems(["contado", "financiado", "tarjeta"])
        self._tipo_pago.setStyleSheet(STYLE_INPUT)
        self._tipo_pago.currentTextChanged.connect(self._toggle_financiacion)
        form.addRow(make_label("Tipo de pago *", size=13, color=TEXT2), self._tipo_pago)

        cl.addLayout(form)

        # ── Panel financiación ──
        self._fin_frame = QFrame()
        self._fin_frame.setStyleSheet(f"""
            QFrame {{
                background: {ACCENT_L};
                border: 1.5px solid #BFDBFE;
                border-radius: 8px;
            }}
        """)
        fl = QFormLayout(self._fin_frame)
        fl.setContentsMargins(24, 20, 24, 20)
        fl.setSpacing(14)
        fl.setLabelAlignment(Qt.AlignRight)
        fl.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        fl.addRow(make_label("Plan de financiación", size=13, bold=True, color=ACCENT))

        self._cuotas = QSpinBox()
        self._cuotas.setRange(1, 84)
        self._cuotas.setValue(12)
        self._cuotas.setSuffix(" meses")
        self._cuotas.setStyleSheet(STYLE_INPUT)

        self._interes = QDoubleSpinBox()
        self._interes.setRange(0, 100)
        self._interes.setDecimals(2)
        self._interes.setSuffix(" %")
        self._interes.setValue(12.0)
        self._interes.setStyleSheet(STYLE_INPUT)

        fl.addRow(make_label("Número de cuotas *", size=13, color=TEXT2), self._cuotas)
        fl.addRow(make_label("Interés anual *", size=13, color=TEXT2), self._interes)

        self._fin_frame.setVisible(False)
        cl.addWidget(self._fin_frame)

        # ── Botones ──
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        btn_limpiar = QPushButton("Limpiar formulario")
        btn_limpiar.setStyleSheet(btn_secondary())
        btn_limpiar.setCursor(Qt.PointingHandCursor)
        btn_limpiar.clicked.connect(self._limpiar)
        btn_row.addWidget(btn_limpiar)

        btn_row.addStretch()

        self._btn_deshacer = QPushButton("↩  Deshacer última venta")
        self._btn_deshacer.setStyleSheet(btn_danger())
        self._btn_deshacer.setCursor(Qt.PointingHandCursor)
        self._btn_deshacer.clicked.connect(self._deshacer)
        btn_row.addWidget(self._btn_deshacer)

        btn_ok = QPushButton("  Registrar venta →")
        btn_ok.setStyleSheet(btn_primary())
        btn_ok.setCursor(Qt.PointingHandCursor)
        btn_ok.clicked.connect(self._registrar)
        btn_row.addWidget(btn_ok)

        cl.addLayout(btn_row)
        layout.addWidget(card)
        layout.addStretch()

        # Carga inicial de combos
        self._cargar_datos()

    def _add_form_row(self, form, label, widget, err_label):
        from PyQt5.QtWidgets import QWidget, QVBoxLayout
        container = QWidget()
        container.setStyleSheet("background: transparent; border: none;")
        vl = QVBoxLayout(container)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(3)
        vl.addWidget(widget)
        vl.addWidget(err_label)
        form.addRow(make_label(label, size=13, color=TEXT2), container)

    def _cargar_datos(self):
        # Clientes
        self._cliente_combo.clear()
        self._cliente_combo.addItem("— Seleccionar cliente —", None)
        try:
            for c in self._ctrl.listar_clientes():
                self._cliente_combo.addItem(
                    f"{c.nombre} {c.apellido} (Cédula: {c.cedula})",
                    c.id_cliente
                )
        except Exception as e:
            show_error(self, f"Error al cargar clientes: {e}")

        # Motos disponibles
        self._moto_combo.clear()
        self._moto_combo.addItem("— Seleccionar moto —", None)
        try:
            for m in self._ctrl.motos_disponibles():
                label = f"[{m.id_moto}] {m.marca} {m.modelo} {m.anio}"
                if m.precio:
                    label += f" — ${m.precio:,.0f}"
                self._moto_combo.addItem(label, m.id_moto)
        except Exception as e:
            show_error(self, f"Error al cargar motos: {e}")

        # Empleados vendedores
        self._empleado_combo.clear()
        self._empleado_combo.addItem("— Seleccionar empleado —", None)
        try:
            for e in self._ctrl.listar_empleados():
                self._empleado_combo.addItem(
                    f"{e.nombre} {e.apellido} ({e.rol})",
                    e.id_empleado
                )
        except Exception as e:
            show_error(self, f"Error al cargar empleados: {e}")

    def _toggle_financiacion(self, tipo):
        self._fin_frame.setVisible(tipo == "financiado")

    def _limpiar(self):
        self._precio.setValue(0)
        self._tipo_pago.setCurrentIndex(0)
        self._cuotas.setValue(12)
        self._interes.setValue(12.0)
        self._cargar_datos()
        # Reset errores
        for w in (self._cliente_combo, self._moto_combo, self._empleado_combo, self._precio):
            w.setStyleSheet(STYLE_INPUT)
        for lbl in (self._err_cliente, self._err_moto, self._err_empleado, self._err_precio):
            lbl.setVisible(False)

    def _validate(self):
        ok = True

        def check(widget, err, condition, msg):
            nonlocal ok
            if not condition:
                widget.setStyleSheet(STYLE_INPUT_ERROR)
                err.setText(msg)
                err.setVisible(True)
                ok = False
            else:
                widget.setStyleSheet(STYLE_INPUT)
                err.setVisible(False)

        check(self._cliente_combo, self._err_cliente,
              self._cliente_combo.currentData() is not None,
              "Selecciona un cliente.")
        check(self._moto_combo, self._err_moto,
              self._moto_combo.currentData() is not None,
              "Selecciona una moto disponible.")
        check(self._empleado_combo, self._err_empleado,
              self._empleado_combo.currentData() is not None,
              "Selecciona un empleado.")
        check(self._precio, self._err_precio,
              self._precio.value() > 0,
              "El precio debe ser mayor a $0.")
        return ok

    def _registrar(self):
        from model.VO.VentaVO import VentaVO
        from model.VO.FinanciacionVO import FinanciacionVO

        if not self._validate():
            return

        venta = VentaVO(
            id_venta=0,
            precio_final=self._precio.value(),
            tipo_pago=self._tipo_pago.currentText(),
            id_cliente=self._cliente_combo.currentData(),
            id_moto=self._moto_combo.currentData(),
            id_empleado=self._empleado_combo.currentData(),
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
            show_ok(self, f"¡Venta #{id_v} registrada exitosamente!")
            self._limpiar()
            self.venta_registrada.emit()
        except Exception as e:
            show_error(self, str(e))

    def _deshacer(self):
        try:
            ok = self._ctrl.deshacer_venta()
            if ok:
                show_ok(self, "Última venta deshecha correctamente.")
                self._cargar_datos()
                self.venta_registrada.emit()
            else:
                show_error(self, "No hay ventas para deshacer.")
        except Exception as e:
            show_error(self, str(e))

    def refresh(self):
        """Recarga los combos (llamar al volver a esta página)."""
        self._cargar_datos()
