import abc
from typing import Annotated, Optional

from fastapi import Depends
from sqlalchemy import Connection

from app.infrastructure.db import engine
from app.shared.base_schema import BaseSchema


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
    def __call__(self, *args, **kwargs) -> Optional[BaseSchema]:
        pass
