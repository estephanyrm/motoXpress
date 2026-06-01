import sys
import os
from random import randint, choice

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from model.VO.VentaVO import VentaVO
from model.VO.FinanciacionVO import FinanciacionVO

from model.DAO.VentaDAO import VentaDAO
from model.DAO.MotoDAO import MotoDAO

# Obtener motos disponibles
motos = MotoDAO.listar_disponibles()

if len(motos) < 10:
    raise Exception("Se necesitan al menos 10 motos disponibles.")

for i, moto in enumerate(motos[:10], start=1):

    id_cliente = randint(1, 20)
    id_empleado = randint(1, 10)

    # Alternar entre contado y financiado
    if i % 2 == 0:

        financiacion = FinanciacionVO(
            id_financiacion=None,
            cuotas=choice([12, 24, 36]),
            interes=choice([8, 10, 12]),
            monto_cuota=0
        )

        venta = VentaVO(
            id_venta=0,
            precio_final=moto.precio,
            tipo_pago="financiado",
            id_cliente=id_cliente,
            id_moto=moto.id_moto,
            id_empleado=id_empleado,
            financiacion=financiacion
        )

        financiacion.monto_cuota = round(
            venta.precio_final *
            (1 + financiacion.interes / 100)
            / financiacion.cuotas,
            2
        )

    else:

        venta = VentaVO(
            id_venta=0,
            precio_final=moto.precio,
            tipo_pago="contado",
            id_cliente=id_cliente,
            id_moto=moto.id_moto,
            id_empleado=id_empleado
        )

    VentaDAO.insertar(venta)

print("Ventas de prueba creadas correctamente.")