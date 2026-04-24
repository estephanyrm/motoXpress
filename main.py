from db.gestor_conexiones import ConexionSQLite3

from model.COMMAND.UndoRedoManager import UndoRedoManager

def connection_factory():
    return ConexionSQLite3("db/concesionario.db")

def build_controller():
    pass

def main():
    pass

if __name__ == "__main__":
    main()