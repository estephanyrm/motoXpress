import psycopg
from psycopg import Connection
from psycopg.rows import dict_row, DictRow

from types import TracebackType
from typing import Any

# Context manager para conexiones PostgreSQL
class ConexionPostgres:
    def __init__(
        self,
        host: str,
        port: str,
        dbname: str,
        user: str,
        password: str
    ):
        self.connection_uri = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        self.connection: Connection[DictRow] | None = None

    def __enter__(self) -> "ConexionPostgres":
        self.connection = psycopg.connect(
            conninfo=self.connection_uri,
            row_factory=dict_row  
        )
        return self
    
    def __exit__(
        self,
        exec_type: type[BaseException] | None,
        exec: BaseException | None,
        traceback: TracebackType | None
    ) -> bool | None:
        if self.connection is None:
            return
        
        if exec_type is None:
            self.connection.commit()

        else:
            self.connection.rollback()
        
        self.connection.close()
        self.connection = None

        return False
    
    def __getattr__(self, name) -> Any:
        if self.connection is None:
            raise AttributeError("Connection not initialized")
        return getattr(self.connection, name)