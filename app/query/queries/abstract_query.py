import abc

from fastapi import Depends
from sqlalchemy import Connection
from starlette.requests import Request


def get_connection(request: Request):
    engine = request.state.engine

    with engine.connect() as connection:
        yield connection


class AbstractQuery(abc.ABC):
    def __init__(self, connection: Connection = Depends(get_connection)):
        self._connection = connection

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass
