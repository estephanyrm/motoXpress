from typing import List

class UndoRedoManager:    
    """
    Clase para el control de estados del sistema
    - Solamente debe existir una instancia en el SI
    - Este vivirá en la RAM (activo solamente en tiempo de ejecución)
    TODO: Implementar persistencia (archivos)
    """
    
    def __init__(self):
        self.undo_stack: List = [] 
        self.redo_stack: List = [] 
        
    def register(self, command):
        self.undo_stack.append(command)
        self.redo_stack.clear()
        
    def push_redo(self, command):
        self.redo_stack.append(command)
        
    def push_undo(self, command):
        self.undo_stack.append(command)
        
    def get_undo(self):
        if not self.undo_stack:
            return None        
        return self.undo_stack.pop()
    
    def get_redo(self):
        if not self.redo_stack:
            return None        
        return self.redo_stack.pop()
        
        
        
     