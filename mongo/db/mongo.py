import mongoengine

def conectar():
    mongoengine.connect(
        db="MotoXpress",
        host="mongodb://localhost:27050"
    )
