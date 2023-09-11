import abc
from typing import Any, Generic, Optional, Sequence, TypeVar

from sqlalchemy import Engine, Executable, Row

Q = TypeVar("Q")
QR = TypeVar("QR")


# TODO: Back-propagate this to other modules
class BaseSQLQuery(Generic[Q, QR], metaclass=abc.ABCMeta):
    def __init__(self, engine: Engine):
        self._engine = engine

    @abc.abstractmethod
    def __call__(self, query: Q) -> QR:
        raise NotImplementedError

    def _first_from(self, query: Executable) -> Optional[Row[Any]]:
        with self._engine.connect() as connection:
            return connection.execute(query).first()

    def _all_from(self, query: Executable) -> Sequence[Row[Any]]:
        with self._engine.connect() as connection:
            return connection.execute(query).all()
