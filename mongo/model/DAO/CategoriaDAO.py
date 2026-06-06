from typing import List, Optional
from mongo.model.VO.CategoriaDocumento import CategoriaDocumento
from mongo.model.VO.CategoriaVO import CategoriaVO

class CategoriaDAO:

    @staticmethod
    def listar_todas() -> List[CategoriaDocumento]:
        # Eager carga todos los documentos de una vez
        return list(CategoriaDocumento.objects.all())

    @staticmethod
    def obtener_por_id(id_categoria: int) -> Optional[CategoriaDocumento]:
        return CategoriaDocumento.objects(id_categoria=id_categoria).first()

    @staticmethod
    def insertar(nombre: str, descripcion: str = None) -> int:
        ultimo = CategoriaDocumento.objects.order_by("-id_categoria").first()
        nuevo_id = (ultimo.id_categoria + 1) if ultimo else 1
        doc = CategoriaDocumento(
            id_categoria=nuevo_id,
            nombre=nombre,
            descripcion=descripcion
        )
        doc.save()
        return nuevo_id

    @staticmethod
    def actualizar(id_categoria: int, nombre: str, descripcion: str = None) -> None:
        CategoriaDocumento.objects(id_categoria=id_categoria).update_one(
            set__nombre=nombre,
            set__descripcion=descripcion
        )

    @staticmethod
    def eliminar(id_categoria: int) -> None:
        CategoriaDocumento.objects(id_categoria=id_categoria).delete()
