from typing import List

from app.services.projects.domain.entities import Project
from app.services.projects.domain.ports import AbstractUnitOfWork
from app.services.projects.test_utils.fake_repository import FakeRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    repository: FakeRepository
    committed = False

    def __init__(self, projects: List[Project]):
        self.repository = FakeRepository(projects=projects)

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
