from app.modules.projects.domain.entities import Project
from app.modules.projects.domain.ports import AbstractRepository, AbstractUnitOfWork
from app.modules.projects.domain.testing.fake_repository import FakeRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    repository: FakeRepository
    committed = False

    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
