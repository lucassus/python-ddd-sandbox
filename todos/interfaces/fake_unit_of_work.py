from typing import List

from todos.domain.models import Task
from todos.interfaces.abstract_repository import AbstractRepository
from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork
from todos.interfaces.fake_repository import FakeRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    committed: False

    def __init__(self, tasks: List[Task]):
        self._tasks = tasks

    def commit(self):
        self.committed = True

    def rollback(self):
        pass

    # TODO: Do not use this pattern
    @property
    def repository(self) -> AbstractRepository:
        return FakeRepository(self._tasks)
