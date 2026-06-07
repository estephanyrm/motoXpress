from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton,
    QComboBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from ui.styles import (
    STYLE_TABLE, STYLE_INPUT, STYLE_INPUT_ERROR,
    ACCENT, SUCCESS, WARNING, DANGER, TEXT, TEXT2, TEXT3,
    WHITE, BORDER, PANEL, btn_primary, btn_secondary, card_style
)
from ui.widgets import make_label, make_divider, show_error


class VentasPage(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self._ctrl = controller
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        layout.addWidget(make_label("Historial de Ventas", size=20, bold=True))
        layout.addWidget(make_label("Filtra por cliente o marca de moto", size=13, color=TEXT2))

        # ── Panel de filtros ──
        filter_card = QFrame()
        filter_card.setStyleSheet(f"""
            QFrame {{
                background: {WHITE};
                border: 1.5px solid {BORDER};
                border-radius: 10px;
            }}
        """)
        fl = QVBoxLayout(filter_card)
        fl.setContentsMargins(24, 20, 24, 20)
        fl.setSpacing(16)

        fl.addWidget(make_label("Filtros de búsqueda", size=13, bold=True))

        row1 = QHBoxLayout()
        row1.setSpacing(14)

        # Filtro por cliente (combo)
        row1.addWidget(make_label("Cliente:", size=13, color=TEXT2))
        self._combo_cliente = QComboBox()
        self._combo_cliente.setStyleSheet(STYLE_INPUT)
        self._combo_cliente.setFixedWidth(260)
        row1.addWidget(self._combo_cliente)

        row1.addWidget(make_divider(vertical=True))
        row1.addSpacing(4)

        # Filtro por marca
        row1.addWidget(make_label("Marca:", size=13, color=TEXT2))
        self._combo_marca = QComboBox()
        self._combo_marca.setStyleSheet(STYLE_INPUT)
        self._combo_marca.setFixedWidth(200)
        row1.addWidget(self._combo_marca)

        row1.addStretch()

        btn_filtrar = QPushButton("  Aplicar filtros")
        btn_filtrar.setStyleSheet(btn_primary())
        btn_filtrar.setCursor(Qt.PointingHandCursor)
        btn_filtrar.setFixedHeight(38)
        btn_filtrar.clicked.connect(self._filtrar)
        row1.addWidget(btn_filtrar)

        btn_reset = QPushButton("Limpiar")
        btn_reset.setStyleSheet(btn_secondary())
        btn_reset.setCursor(Qt.PointingHandCursor)
        btn_reset.setFixedHeight(38)
        btn_reset.clicked.connect(self._reset)
        row1.addWidget(btn_reset)

        fl.addLayout(row1)

        self._hint = make_label(
            "Consejo: Si seleccionas un cliente específico, el filtro de marca se ignora.",
            size=11, color=TEXT3, italic=True
        )
        fl.addWidget(self._hint)

        layout.addWidget(filter_card)

        # ── Tabla ──
        cols = ["ID", "Fecha", "Moto", "Precio", "Tipo pago", "Cliente", "Empleado"]
        self._tbl = QTableWidget(0, len(cols))
        self._tbl.setStyleSheet(STYLE_TABLE)
        self._tbl.setHorizontalHeaderLabels(cols)
        hh = self._tbl.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.Stretch)
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self._tbl.setEditTriggers(QTableWidget.NoEditTriggers)
        self._tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self._tbl.verticalHeader().setVisible(False)
        self._tbl.setFocusPolicy(Qt.NoFocus)
        self._tbl.setAlternatingRowColors(True)
        self._tbl.setSortingEnabled(False)  # el orden lo controla la BD (DESC)
        layout.addWidget(self._tbl)

        self._load_clientes()
        self._load_marcas()
        self._reset()

    def _load_clientes(self):
        self._combo_cliente.clear()
        self._combo_cliente.addItem("Todos los clientes", None)
        try:
            for c in self._ctrl.listar_clientes():
                self._combo_cliente.addItem(
                    f"{c.nombre} {c.apellido} (Cédula: {c.cedula})",
                    c.id_cliente
                )
        except Exception as e:
            show_error(self, str(e))

    def _load_marcas(self):
        self._combo_marca.clear()
        self._combo_marca.addItem("Todas las marcas", None)
        try:
            motos = self._ctrl.todas_las_motos()
            marcas_vistas = set()
            for m in sorted(motos, key=lambda m: m.marca or ""):
                if m.marca and m.marca not in marcas_vistas:
                    marcas_vistas.add(m.marca)
                    self._combo_marca.addItem(m.marca, m.marca)
        except Exception as e:
            show_error(self, str(e))

    def _reset(self):
        self._combo_cliente.setCurrentIndex(0)
        self._combo_marca.setCurrentIndex(0)
        self._filtrar()

    def _filtrar(self):
        id_cli = self._combo_cliente.currentData()
        marca = self._combo_marca.currentData()
        try:
            if id_cli is not None:
                ventas = self._ctrl.ventas_por_cliente(id_cli)
            elif marca is not None:
                ventas = self._ctrl.ventas_por_marca(marca)
            else:
                ventas = self._ctrl.listar_todas_ventas()
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

            fecha = str(v.fecha_venta or "")[:10]
            self._tbl.setItem(i, 1, QTableWidgetItem(fecha))

            # Moto con nombre completo
            moto_txt = ""
            try:
                if v._moto_cache:
                    moto_txt = f"{v._moto_cache.marca} {v._moto_cache.modelo}"
                elif v.id_moto:
                    moto_txt = f"ID {v.id_moto}"
            except Exception:
                moto_txt = str(v.id_moto or "")
            self._tbl.setItem(i, 2, QTableWidgetItem(moto_txt))

            precio_item = QTableWidgetItem(
                f"${v.precio_final:,.0f}" if v.precio_final else "—"
            )
            precio_item.setForeground(QColor(SUCCESS))
            self._tbl.setItem(i, 3, precio_item)

            tipo = v.tipo_pago or ""
            tp_item = QTableWidgetItem(tipo.capitalize())
            tp_item.setForeground(QColor(tipo_colors.get(tipo, TEXT2)))
            self._tbl.setItem(i, 4, tp_item)

            # Cliente: mostrar nombre si está disponible
            cli_txt = str(v.id_cliente or "")
            try:
                if v._cliente_cache:
                    cli_txt = f"{v._cliente_cache.nombre} {v._cliente_cache.apellido}"
            except Exception:
                pass
            self._tbl.setItem(i, 5, QTableWidgetItem(cli_txt))

            # Empleado
            emp_txt = str(v.id_empleado or "")
            try:
                if v._empleado_cache:
                    emp_txt = f"{v._empleado_cache.nombre} {v._empleado_cache.apellido}"
            except Exception:
                pass
            self._tbl.setItem(i, 6, QTableWidgetItem(emp_txt))

        self._tbl.resizeRowsToContents()

    def refresh(self):
        self._load_clientes()
        self._load_marcas()