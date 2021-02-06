import abc

from databases import Database
from fastapi import Depends

from app.query.queries.database import get_database


class AbstractQuery(abc.ABC):
    def __init__(self, database: Database = Depends(get_database)):
        self._database = database

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass
