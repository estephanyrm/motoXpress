import sqlite3
from sqlite3 import Connection
from typing import Optional

class ConexionSQLite3:
    
    def __init__(self, db_path: str='./'):
        self.db_path = db_path
        self.conn: Optional[Connection] = None
    
    def __enter__(self)->Connection:
        """Lo que se va a realizar y lo que se va a cargar en with/as"""
               
        self.conn = sqlite3.connect(self.db_path)        
        
        # Acceder a las columnas por el nombre que tienen en el DDL
        self.conn.row_factory = sqlite3.Row  
        
        print("ENTER -> conexión abierta!!!!")
        
        return self.conn
    
    def __exit__(self, exec_type, exec, tb)->bool:
        """Acciones:
        - Lo que se va a realizar cuando se termine el contexto 
        - O cuando haya un fallo en el contexto
        """
        
        # Salida exitosa del contexto
        if exec_type is None:
            
            print("EXIT -> COMMIT")
            
            # Quiero confirmar las transacciones realizadas
            self.conn.commit()
        
        # Acciones cuando se presente el fallo
        else:            
            
            print("EXIT -> Deshaciendo cambios por error")
            print(f"Tipo de excepción -> {exec_type}")
            print(f"Excepción -> {exec}")
            
            # Quiero evitar que se guarden los cambios
            self.conn.rollback()
        
        # Lo que siempre se va a hacer sin importar si hay o no hay fallo
        self.conn.close()
        
        return False