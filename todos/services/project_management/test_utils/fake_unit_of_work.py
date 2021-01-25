from typing import List

from todos.services.project_management.domain.entities import Project
from todos.services.project_management.domain.ports import AbstractUnitOfWork
from todos.services.project_management.test_utils.fake_repository import FakeRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    repository: FakeRepository
    committed = False

    def __init__(self, projects: List[Project]):
        self.repository = FakeRepository(projects=projects)

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
