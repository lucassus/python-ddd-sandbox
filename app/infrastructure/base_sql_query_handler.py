import abc
from typing import Any, Generic, Optional, Sequence, TypeVar

from sqlalchemy import Executable, Row
from sqlalchemy.ext.asyncio import AsyncEngine

from app.shared.query import Query

Q = TypeVar("Q", bound=Query)
QR = TypeVar("QR")


class BaseSQLQueryHandler(Generic[Q, QR], metaclass=abc.ABCMeta):
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

    @abc.abstractmethod
    async def __call__(self, query: Q) -> QR:
        raise NotImplementedError

    async def _first_from(self, stmt: Executable) -> Optional[Row[Any]]:
        async with self._engine.connect() as connection:
            result = await connection.execute(stmt)
            return result.first()

    async def _all_from(self, stmt: Executable) -> Sequence[Row[Any]]:
        async with self._engine.connect() as connection:
            result = await connection.execute(stmt)
            return result.all()
