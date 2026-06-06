import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mongo.db.mongo import conectar
conectar()

from random import choice

from postgres.db.postgres import ConexionPostgres
from postgres.model.DAO.ClienteDAO import ClienteDAO
from postgres.model.DAO.EmpleadoDAO import EmpleadoDAO
from postgres.model.VO.ClienteVO import ClienteVO
from postgres.model.VO.EmpleadoVO import EmpleadoVO

from mongo.model.DAO.MotoDAO import MotoDAO
from mongo.model.DAO.CategoriaDAO import CategoriaDAO
from mongo.model.VO.MotoVO import MotoVO
from mongo.model.VO.CategoriaVO import CategoriaVO

_PG = ConexionPostgres(
    host="localhost", port="5433",
    dbname="motoxpress", user="root", password="2007"
)

print("Cargando datos de prueba...")

# CATEGORIAS (Mongo con mongoengine)
categorias = CategoriaDAO.listar_todas()
if not categorias:
    print("Creando categorías...")
    for nombre in ["Deportiva", "Trail", "Scooter"]:
        CategoriaDAO.insertar(nombre=nombre, descripcion=f"Motos de tipo {nombre}")
    categorias = CategoriaDAO.listar_todas()

# CLIENTES (PostgreSQL con psycopg)
clientes_data = [
    ("Juan","Pérez"),("Ana","Gómez"),("Carlos","Ruiz"),("Laura","Torres"),
    ("David","Martínez"),("Sofía","Castro"),("Miguel","Rojas"),("Valentina","López"),
    ("Daniel","Moreno"),("Camila","Hernández"),("Andrés","Vargas"),("Paula","Gil"),
    ("Mateo","Cruz"),("Juliana","Ramírez"),("Sebastián","Mejía"),("Natalia","Cardona"),
    ("Felipe","Restrepo"),("Sara","Muñoz"),("Tomás","Jaramillo"),("Isabella","Quintero")
]
with _PG as conn:
    for i, (nombre, apellido) in enumerate(clientes_data, start=1):
        ClienteDAO.insertar(conn, ClienteVO(
            id_cliente=0, nombre=nombre, apellido=apellido,
            cedula=f"100000{i}", telefono=f"300555{i:04}",
            email=f"{nombre.lower()}.{apellido.lower()}@correo.com"
        ))
print("Clientes creados")

# EMPLEADOS (PostgreSQL con psycopg)
empleados_data = [
    ("Juan","Pérez","Vendedor"),("Ana","Gómez","Gerente"),("Carlos","Ruiz","Vendedor"),
    ("Laura","Torres","Asesor"),("David","Martínez","Vendedor"),("Paula","Gil","Asesor"),
    ("Mateo","Cruz","Vendedor"),("Natalia","Cardona","Gerente"),
    ("Felipe","Restrepo","Asesor"),("Sara","Muñoz","Vendedor")
]
with _PG as conn:
    for nombre, apellido, rol in empleados_data:
        EmpleadoDAO.insertar(conn, EmpleadoVO(
            id_empleado=0, nombre=nombre, apellido=apellido, rol=rol,
            email=f"{nombre.lower()}.{apellido.lower()}@motoxpress.com"
        ))
print("Empleados creados")

# MOTOS (Mongo con mongoengine)
motos_data = [
    ("Yamaha","MT-03"),("Yamaha","R15"),("Yamaha","FZ25"),("Honda","CB190R"),
    ("Honda","CB300F"),("Honda","XR190L"),("Suzuki","Gixxer 250"),("Suzuki","GSX-S150"),
    ("Suzuki","V-Strom 250"),("Kawasaki","Z400"),("Kawasaki","Ninja 400"),
    ("Kawasaki","Versys X300"),("BMW","G310R"),("BMW","G310GS"),("KTM","Duke 200"),
    ("KTM","Duke 390"),("Bajaj","Dominar 400"),("Bajaj","Pulsar N250"),
    ("TVS","Apache RTR 200"),("Royal Enfield","Hunter 350")
]
for i, (marca, modelo) in enumerate(motos_data, start=1):
    cat = choice(categorias)
    moto = MotoVO(
        vin=f"VIN{i:05}", marca=marca, modelo=modelo,
        anio=2022+(i%3), precio=15000000+(i*1200000),
        color=choice(["Negro","Rojo","Azul","Blanco","Gris"]),
        estado="disponible",
        categorias=[cat.to_embedded()]
    )
    MotoDAO.insertar(moto)
print("Motos creadas")
print("Base de datos poblada correctamente")
