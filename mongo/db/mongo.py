import mongoengine

def conectar():
    mongoengine.connect(
        db="MotoXpress",
        host="mongodb://localhost:27117,localhost:27118,localhost:27119/?replicaSet=replicaSet"
    )
