import mongoengine
from mongo.model.VO.CategoriaVO import CategoriaVO as CategoriaEmbedded

class CategoriaDocumento(mongoengine.Document):
    meta = {"collection": "Categoria"}

    id_categoria = mongoengine.IntField(required=True, unique=True)
    nombre = mongoengine.StringField(required=True)
    descripcion = mongoengine.StringField()

    def to_embedded(self) -> CategoriaEmbedded:
        return CategoriaEmbedded(
            id_categoria=self.id_categoria,
            nombre=self.nombre,
            descripcion=self.descripcion
        )
