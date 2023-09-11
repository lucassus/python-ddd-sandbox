import abc
from typing import Any, Generic, Optional, Sequence, TypeVar

from sqlalchemy import Engine, Executable, Row

from app.shared.query import Query

Q = TypeVar("Q", bound=Query)
QR = TypeVar("QR")


class BaseSQLQueryHandler(Generic[Q, QR], metaclass=abc.ABCMeta):
    def __init__(self, engine: Engine):
        self._engine = engine

    @abc.abstractmethod
    def __call__(self, query: Q) -> QR:
        raise NotImplementedError

    def _first_from(self, stmt: Executable) -> Optional[Row[Any]]:
        with self._engine.connect() as connection:
            return connection.execute(stmt).first()

    def _all_from(self, stmt: Executable) -> Sequence[Row[Any]]:
        with self._engine.connect() as connection:
            return connection.execute(stmt).all()
