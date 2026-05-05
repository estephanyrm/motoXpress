from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton,
    QLineEdit, QDialog, QFormLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from ui.styles import (
    STYLE_TABLE, STYLE_INPUT, STYLE_INPUT_ERROR,
    ACCENT, SUCCESS, TEXT, TEXT2, TEXT3, DANGER,
    WHITE, BORDER, btn_primary, btn_secondary
)
from ui.widgets import make_label, make_divider, show_error, show_ok


class ClientesPage(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self._ctrl = controller
        self._all_clientes = []
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
        hv.addWidget(make_label("Clientes", size=20, bold=True))
        hv.addWidget(make_label("Listado de clientes registrados", size=13, color=TEXT2))
        header.addLayout(hv)
        header.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("Buscar por nombre o cédula…")
        self._search.setFixedWidth(250)
        self._search.setStyleSheet(STYLE_INPUT)
        self._search.textChanged.connect(self._filter)
        header.addWidget(self._search)

        btn_reg = QPushButton("  + Registrar cliente")
        btn_reg.setStyleSheet(btn_primary())
        btn_reg.setCursor(Qt.PointingHandCursor)
        btn_reg.setFixedHeight(38)
        btn_reg.clicked.connect(self._form_registrar)
        header.addWidget(btn_reg)
        layout.addLayout(header)

        # ── Tabla ──
        cols = ["ID", "Nombre", "Apellido", "Cédula", "Teléfono", "Email", "Registro"]
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
        layout.addWidget(self._tbl)

        self._reload()

    def _reload(self):
        try:
            self._all_clientes = self._ctrl.listar_clientes()
        except Exception as e:
            show_error(self, str(e))
            self._all_clientes = []
        self._filter(self._search.text())

    def _filter(self, text):
        t = text.lower().strip()
        if not t:
            self._populate(self._all_clientes)
            return
        result = [
            c for c in self._all_clientes
            if t in (c.nombre or "").lower()
            or t in (c.apellido or "").lower()
            or t in (c.cedula or "").lower()
            or t in (c.email or "").lower()
        ]
        self._populate(result)

    def _populate(self, clientes):
        self._tbl.setRowCount(len(clientes))
        for i, c in enumerate(clientes):
            self._tbl.setItem(i, 0, QTableWidgetItem(str(c.id_cliente)))
            self._tbl.setItem(i, 1, QTableWidgetItem(c.nombre or ""))
            self._tbl.setItem(i, 2, QTableWidgetItem(c.apellido or ""))
            self._tbl.setItem(i, 3, QTableWidgetItem(c.cedula or ""))
            self._tbl.setItem(i, 4, QTableWidgetItem(c.telefono or "—"))
            self._tbl.setItem(i, 5, QTableWidgetItem(c.email or "—"))
            fecha = ""
            if c.fecha_registro:
                try:
                    fecha = str(c.fecha_registro)[:10]
                except Exception:
                    fecha = str(c.fecha_registro)
            self._tbl.setItem(i, 6, QTableWidgetItem(fecha))
        self._tbl.resizeRowsToContents()

    def _form_registrar(self):
        dlg = _ClienteDialog(self, self._ctrl)
        if dlg.exec_() == QDialog.Accepted:
            self._reload()


#  Diálogo: Registrar cliente
class _ClienteDialog(QDialog):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self._ctrl = controller
        self.setWindowTitle("Registrar cliente")
        self.setMinimumWidth(440)
        self.setStyleSheet(f"QDialog {{ background: {WHITE}; }}")
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        layout.addWidget(make_label("Nuevo cliente", size=17, bold=True))
        layout.addWidget(make_label("Los campos con * son obligatorios.", size=12, color=TEXT2))
        layout.addWidget(make_divider())

        form = QFormLayout()
        form.setSpacing(14)
        form.setLabelAlignment(Qt.AlignRight)
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        def field(ph=""):
            w = QLineEdit()
            w.setPlaceholderText(ph)
            w.setStyleSheet(STYLE_INPUT)
            return w

        self._nombre   = field("ej. Carlos")
        self._apellido = field("ej. Ramírez")
        self._cedula   = field("ej. 1234567890")
        self._telefono = field("ej. 3001234567")
        self._email    = field("ej. carlos@email.com")

        self._err_nombre   = self._add_row(form, "Nombre *",   self._nombre)
        self._err_apellido = self._add_row(form, "Apellido *", self._apellido)
        self._err_cedula   = self._add_row(form, "Cédula *",   self._cedula)
        self._add_row(form, "Teléfono", self._telefono)
        self._add_row(form, "Email",    self._email)
        layout.addLayout(form)

        layout.addSpacing(8)
        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(btn_secondary())
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_cancel)
        btn_row.addStretch()
        btn_save = QPushButton("  Registrar")
        btn_save.setStyleSheet(btn_primary())
        btn_save.clicked.connect(self._save)
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _add_row(self, form, label, widget):
        from PyQt5.QtWidgets import QWidget, QVBoxLayout
        container = QWidget()
        container.setStyleSheet("background: transparent; border: none;")
        vl = QVBoxLayout(container)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(3)
        vl.addWidget(widget)
        err = make_label("", size=11, color=DANGER)
        err.setVisible(False)
        vl.addWidget(err)
        form.addRow(make_label(label, size=13, color=TEXT2), container)
        return err

    def _validate(self):
        ok = True

        def check(w, err, cond, msg):
            nonlocal ok
            if not cond:
                w.setStyleSheet(STYLE_INPUT_ERROR)
                err.setText(msg)
                err.setVisible(True)
                ok = False
            else:
                w.setStyleSheet(STYLE_INPUT)
                err.setVisible(False)

        check(self._nombre,   self._err_nombre,
              bool(self._nombre.text().strip()),   "El nombre es obligatorio.")
        check(self._apellido, self._err_apellido,
              bool(self._apellido.text().strip()), "El apellido es obligatorio.")
        check(self._cedula,   self._err_cedula,
              bool(self._cedula.text().strip()),   "La cédula es obligatoria.")
        return ok

    def _save(self):
        from model.VO.ClienteVO import ClienteVO
        if not self._validate():
            return
        try:
            c = ClienteVO(
                id_cliente=0,
                nombre=self._nombre.text().strip().title(),
                apellido=self._apellido.text().strip().title(),
                cedula=self._cedula.text().strip(),
                telefono=self._telefono.text().strip() or None,
                email=self._email.text().strip() or None,
            )
            self._ctrl.registrar_cliente(c)
            show_ok(self, "Cliente registrado exitosamente.")
            self.accept()
        except Exception as e:
            show_error(self, str(e))
