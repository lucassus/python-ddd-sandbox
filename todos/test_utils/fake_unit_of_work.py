from typing import List

from todos.domain.models import Project
from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork
from todos.test_utils.fake_repository import FakeRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    repository: FakeRepository
    committed: False

    def __init__(self, projects: List[Project]):
        self.repository = FakeRepository(projects=projects)

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
