from typing import List

from todos.domain.models import Task
from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork
from todos.test_utils.fake_repository import FakeRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    repository: FakeRepository
    committed: False

    def __init__(self, tasks: List[Task]):
        self.repository = FakeRepository(tasks=tasks)

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
