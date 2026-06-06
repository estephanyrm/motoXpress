from typing import List, Optional
from mongo.model.VO.MotoVO import MotoVO
from mongo.model.VO.CategoriaVO import CategoriaVO

class MotoDAO:

    @staticmethod
    def listar_disponibles() -> List[MotoVO]:
        # Eager trae todos los campos incluidas las categorias embebidas
        return list(MotoVO.objects(estado="disponible"))

    @staticmethod
    def obtener_por_id(id_moto: int) -> Optional[MotoVO]:
        # Lazy solo se ejecuta cuando se necesita el documento
        return MotoVO.objects(id_moto=id_moto).first()

    @staticmethod
    def buscar_por_vin(vin: str) -> Optional[MotoVO]:
        return MotoVO.objects(vin=vin).first()

    @staticmethod
    def insertar(moto: MotoVO) -> int:
        ultimo = MotoVO.objects.order_by("-id_moto").first()
        nuevo_id = (ultimo.id_moto + 1) if ultimo else 1
        moto.id_moto = nuevo_id
        moto.save()
        return nuevo_id

    @staticmethod
    def actualizar_estado(id_moto: int, nuevo_estado: str) -> None:
        MotoVO.objects(id_moto=id_moto).update_one(set__estado=nuevo_estado)
