import sys
import os

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from random import choice

from model.DAO.ClienteDAO import ClienteDAO
from model.DAO.EmpleadoDAO import EmpleadoDAO
from model.DAO.MotoDAO import MotoDAO
from model.DAO.CategoriaDAO import CategoriaDAO

from model.VO.ClienteVO import ClienteVO
from model.VO.EmpleadoVO import EmpleadoVO
from model.VO.MotoVO import MotoVO
from model.VO.CategoriaVO import CategoriaVO


print("Cargando datos de prueba...")

# CATEGORIAS EXISTENTES

categorias = CategoriaDAO.listar_todas()

if not categorias:
    print("No existen categorías. Creando por defecto...")
    for nombre in ["Deportiva", "Trail", "Scooter"]:
        CategoriaDAO.insertar(
            CategoriaVO(
                id_categoria=0, 
                nombre=nombre, 
                descripcion=f"Motos de tipo {nombre}"
            )
        )

# CLIENTES

clientes = [
    ("Juan", "Pérez"),
    ("Ana", "Gómez"),
    ("Carlos", "Ruiz"),
    ("Laura", "Torres"),
    ("David", "Martínez"),
    ("Sofía", "Castro"),
    ("Miguel", "Rojas"),
    ("Valentina", "López"),
    ("Daniel", "Moreno"),
    ("Camila", "Hernández"),
    ("Andrés", "Vargas"),
    ("Paula", "Gil"),
    ("Mateo", "Cruz"),
    ("Juliana", "Ramírez"),
    ("Sebastián", "Mejía"),
    ("Natalia", "Cardona"),
    ("Felipe", "Restrepo"),
    ("Sara", "Muñoz"),
    ("Tomás", "Jaramillo"),
    ("Isabella", "Quintero")
]

for i, (nombre, apellido) in enumerate(clientes, start=1):

    cliente = ClienteVO(
        id_cliente=0,
        nombre=nombre,
        apellido=apellido,
        cedula=f"100000{i}",
        telefono=f"300555{i:04}",
        email=f"{nombre.lower()}.{apellido.lower()}@correo.com"
    )

    ClienteDAO.insertar(cliente)

print("Clientes creados")

# EMPLEADOS

empleados = [
    ("Juan", "Pérez", "Vendedor"),
    ("Ana", "Gómez", "Gerente"),
    ("Carlos", "Ruiz", "Vendedor"),
    ("Laura", "Torres", "Asesor"),
    ("David", "Martínez", "Vendedor"),
    ("Paula", "Gil", "Asesor"),
    ("Mateo", "Cruz", "Vendedor"),
    ("Natalia", "Cardona", "Gerente"),
    ("Felipe", "Restrepo", "Asesor"),
    ("Sara", "Muñoz", "Vendedor")
]

for nombre, apellido, rol in empleados:

    empleado = EmpleadoVO(
        id_empleado=0,
        nombre=nombre,
        apellido=apellido,
        rol=rol,
        email=f"{nombre.lower()}.{apellido.lower()}@motoxpress.com"
    )

    EmpleadoDAO.insertar(empleado)

print("Empleados creados")

# MOTOS

motos = [
    ("Yamaha", "MT-03"),
    ("Yamaha", "R15"),
    ("Yamaha", "FZ25"),
    ("Honda", "CB190R"),
    ("Honda", "CB300F"),
    ("Honda", "XR190L"),
    ("Suzuki", "Gixxer 250"),
    ("Suzuki", "GSX-S150"),
    ("Suzuki", "V-Strom 250"),
    ("Kawasaki", "Z400"),
    ("Kawasaki", "Ninja 400"),
    ("Kawasaki", "Versys X300"),
    ("BMW", "G310R"),
    ("BMW", "G310GS"),
    ("KTM", "Duke 200"),
    ("KTM", "Duke 390"),
    ("Bajaj", "Dominar 400"),
    ("Bajaj", "Pulsar N250"),
    ("TVS", "Apache RTR 200"),
    ("Royal Enfield", "Hunter 350")
]

for i, (marca, modelo) in enumerate(motos, start=1):

    moto = MotoVO(
        id_moto=0,
        vin=f"VIN{i:05}",
        marca=marca,
        modelo=modelo,
        anio=2022 + (i % 3),
        precio=15000000 + (i * 1200000),
        color=choice([
            "Negro",
            "Rojo",
            "Azul",
            "Blanco",
            "Gris"
        ]),
        estado="disponible"
    )

    moto.categorias = [choice(categorias)]

    MotoDAO.insertar(moto)

print("Motos creadas")
print("Base de datos poblada correctamente")