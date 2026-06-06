import json, os
from typing import List

_PERSIST_PATH = "undo_stack.json"

class UndoRedoManager:
    def __init__(self):
        self.undo_stack: List = []
        self.redo_stack: List = []
        self._cargar()

    def register(self, command):
        self.undo_stack.append(command)
        self.redo_stack.clear()
        self._guardar()

    def push_redo(self, command):
        self.redo_stack.append(command)
        self._guardar()

    def push_undo(self, command):
        self.undo_stack.append(command)
        self._guardar()

    def get_undo(self):
        if not self.undo_stack:
            return None
        cmd = self.undo_stack.pop()
        self._guardar()
        return cmd

    def get_redo(self):
        if not self.redo_stack:
            return None
        cmd = self.redo_stack.pop()
        self._guardar()
        return cmd

    def tiene_undo(self) -> bool:
        return len(self.undo_stack) > 0

    def tiene_redo(self) -> bool:
        return len(self.redo_stack) > 0

    def _cmd_to_dict(self, cmd) -> dict:
        from postgres.model.VO.VentaVO import VentaVO
        v = cmd._venta
        f = v.financiacion
        return {
            "venta_id": cmd._venta_id,
            "moto_estado_anterior": cmd._moto_estado_anterior,
            "financiacion_id": cmd._financiacion_id,
            "venta": {
                "id_venta": v.id_venta,
                "precio_final": v.precio_final,
                "tipo_pago": v.tipo_pago,
                "id_cliente": v.id_cliente,
                "id_moto": v.id_moto,
                "id_empleado": v.id_empleado,
            },
            "financiacion": {
                "id_financiacion": f.id_financiacion,
                "cuotas": f.cuotas,
                "interes": f.interes,
                "monto_cuota": f.monto_cuota,
                "id_venta": f.id_venta,
            } if f else None,
        }

    def _dict_to_cmd(self, d: dict):
        from postgres.model.VO.VentaVO import VentaVO
        from postgres.model.VO.FinanciacionVO import FinanciacionVO
        from model.COMMAND.ventas.RegistrarVentaCommand import RegistrarVentaCommand

        vd = d["venta"]
        venta = VentaVO(
            id_venta = vd["id_venta"],
            precio_final = vd["precio_final"],
            tipo_pago = vd["tipo_pago"],
            id_cliente = vd["id_cliente"],
            id_moto = vd["id_moto"],
            id_empleado = vd["id_empleado"],
        )
        financiacion = None
        if d["financiacion"]:
            fd = d["financiacion"]
            financiacion = FinanciacionVO(
                id_financiacion=fd["id_financiacion"],
                cuotas =fd["cuotas"],
                interes =fd["interes"],
                monto_cuota=fd["monto_cuota"],
                id_venta =fd["id_venta"],
            )
            venta.financiacion = financiacion

        cmd = RegistrarVentaCommand(venta)
        cmd._venta_id = d["venta_id"]
        cmd._moto_estado_anterior = d["moto_estado_anterior"]
        cmd._financiacion_id = d["financiacion_id"]
        return cmd

    def _guardar(self):
        data = {
            "undo": [self._cmd_to_dict(c) for c in self.undo_stack],
            "redo": [self._cmd_to_dict(c) for c in self.redo_stack],
        }
        with open(_PERSIST_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _cargar(self):
        if not os.path.exists(_PERSIST_PATH):
            return
        try:
            with open(_PERSIST_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.undo_stack = [self._dict_to_cmd(d) for d in data.get("undo", [])]
            self.redo_stack = [self._dict_to_cmd(d) for d in data.get("redo", [])]
        except Exception:
            self.undo_stack = []
            self.redo_stack = []
