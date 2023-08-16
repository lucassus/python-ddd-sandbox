from typing import Any

from sqlalchemy import Connection, Executable


class BaseSQLQuery:
    def __init__(self, connection: Connection):
        self._connection = connection

    def _first_from(self, query: Executable) -> Any:
        return self._connection.execute(query).first()
