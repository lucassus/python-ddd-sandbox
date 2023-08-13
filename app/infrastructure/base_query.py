from typing import Any

from sqlalchemy import Connection, Executable


class BaseSQLQuery:
    def __init__(self, connection: Connection):
        self._connection = connection

    def _first_from(self, query: Executable) -> Any:
        return self._connection.execute(query).first()

    # TODO: Maybe deprecate this or change to generator
    def _all_from(self, query: Executable) -> list[Any]:
        return list(self._connection.execute(query).all())
