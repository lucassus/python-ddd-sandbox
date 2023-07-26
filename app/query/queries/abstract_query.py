import abc
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import Connection, Executable

from app.infrastructure.db import engine


def get_connection():
    with engine.connect() as connection:
        yield connection


class AbstractQuery(abc.ABC):
    def __init__(
        self,
        connection: Annotated[Connection, Depends(get_connection)],
    ):
        self._connection = connection

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        pass

    def _first_from(self, query: Executable) -> Any:
        return self._connection.execute(query).first()

    def _all_from(self, query: Executable) -> list[Any]:
        return list(self._connection.execute(query).all())
