import psycopg
from psycopg import Connection
from psycopg.rows import dict_row, DictRow

from types import TracebackType
from typing import Any


class ConexionPostgres:
    """
    Context manager para conexiones PostgreSQL

    Uso:
        with.connection_factory() as conn:
            conn.execute(sql, params)

    Al salir del bloque:
        - Sin error  → COMMIT
        - Con error  → ROLLBACK
        - Siempre    → CIERRA 
    """

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
            row_factory=dict_row  # type: ignore
        )

        # Si retorno self.connection en vez de self pylance llora jeje
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
    
    # Para que el type checker no se enloquezca
    def __getattr__(self, name) -> Any:
        if self.connection is None:
            raise AttributeError("Connection not initialized")
        return getattr(self.connection, name)