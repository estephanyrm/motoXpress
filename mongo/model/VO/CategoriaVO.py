import mongoengine

class CategoriaVO(mongoengine.EmbeddedDocument):
    id_categoria = mongoengine.IntField(required=True)
    nombre       = mongoengine.StringField(required=True)
    descripcion  = mongoengine.StringField()
