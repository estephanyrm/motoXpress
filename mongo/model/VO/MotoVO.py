import mongoengine
from mongo.model.VO.CategoriaVO import CategoriaVO

class MotoVO(mongoengine.Document):
    meta = {"collection": "Moto"}

    id_moto = mongoengine.IntField(required=True)
    vin = mongoengine.StringField(required=True)
    marca = mongoengine.StringField(required=True)
    modelo = mongoengine.StringField(required=True)
    anio = mongoengine.IntField(required=True)
    precio = mongoengine.FloatField(required=True)
    color = mongoengine.StringField()
    estado = mongoengine.StringField(default="disponible")

    # categorias viven dentro del documento Moto
    categorias = mongoengine.EmbeddedDocumentListField(CategoriaVO)

    @property
    def esta_disponible(self):
        return self.estado == "disponible"

    def cargar_categorias(self):
        pass
