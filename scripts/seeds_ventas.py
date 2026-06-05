import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from random import randint, choice

from postgres.db.postgres import ConexionPostgres
from postgres.model.DAO.VentaDAO import VentaDAO
from postgres.model.VO.VentaVO import VentaVO
from postgres.model.VO.FinanciacionVO import FinanciacionVO
from mongo.model.DAO.MotoDAO import MotoDAO

_PG = ConexionPostgres(
    host="localhost", port="5433",
    dbname="motoxpress", user="root", password="2007"
)

motos = MotoDAO.listar_disponibles()
if len(motos) < 10:
    raise Exception("Se necesitan al menos 10 motos disponibles.")

with _PG as conn:
    for i, moto in enumerate(motos[:10], start=1):
        id_cliente  = randint(1, 20)
        id_empleado = randint(1, 10)

        if i % 2 == 0:
            financiacion = FinanciacionVO(
                id_financiacion=None,
                cuotas=choice([12, 24, 36]),
                interes=choice([8, 10, 12]),
                monto_cuota=0
            )
            venta = VentaVO(
                id_venta=0, precio_final=moto.precio, tipo_pago="financiado",
                id_cliente=id_cliente, id_moto=moto.id_moto,
                id_empleado=id_empleado, financiacion=financiacion
            )
            financiacion.monto_cuota = round(
                venta.precio_final * (1 + financiacion.interes / 100) / financiacion.cuotas, 2
            )
        else:
            venta = VentaVO(
                id_venta=0, precio_final=moto.precio, tipo_pago="contado",
                id_cliente=id_cliente, id_moto=moto.id_moto, id_empleado=id_empleado
            )

        VentaDAO.insertar(conn, venta)

print("Ventas de prueba creadas correctamente.")
