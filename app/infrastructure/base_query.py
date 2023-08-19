from typing import Any, Optional, Sequence

from sqlalchemy import Engine, Executable, Row


class BaseSQLQuery:
    def __init__(self, engine: Engine):
        self._engine = engine

    def _first_from(self, query: Executable) -> Optional[Row[Any]]:
        with self._engine.connect() as connection:
            return connection.execute(query).first()

    def _all_from(self, query: Executable) -> Sequence[Row[Any]]:
        with self._engine.connect() as connection:
            return connection.execute(query).all()
