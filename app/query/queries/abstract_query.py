import abc
from typing import Optional

from fastapi import Depends
from sqlalchemy import Connection
from starlette.requests import Request

from app.common.base_schema import BaseSchema


def get_connection(request: Request):
    engine = request.state.engine

    with engine.connect() as connection:
        yield connection


class AbstractQuery(abc.ABC):
    def __init__(self, connection: Connection = Depends(get_connection)):
        self._connection = connection

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> Optional[BaseSchema]:
        pass
