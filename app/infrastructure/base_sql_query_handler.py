import abc
from collections.abc import Sequence
from typing import Any

from sqlalchemy import Executable, Row
from sqlalchemy.ext.asyncio import AsyncEngine

from app.shared.query import Query


class BaseSQLQueryHandler[Q: Query, QR](metaclass=abc.ABCMeta):
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

    @abc.abstractmethod
    async def __call__(self, query: Q) -> QR:
        raise NotImplementedError

    async def _first_from(self, stmt: Executable) -> Row[Any] | None:
        async with self._engine.connect() as connection:
            result = await connection.execute(stmt)
            return result.first()

    async def _all_from(self, stmt: Executable) -> Sequence[Row[Any]]:
        async with self._engine.connect() as connection:
            result = await connection.execute(stmt)
            return result.all()
