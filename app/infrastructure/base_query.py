from typing import Any

from sqlalchemy import Engine, Executable


class BaseSQLQuery:
    def __init__(self, engine: Engine):
        self._engine = engine

    def _first_from(self, query: Executable) -> Any:
        with self._engine.connect() as connection:
            return connection.execute(query).first()
