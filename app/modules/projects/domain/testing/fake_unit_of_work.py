from app.modules.projects.domain.ports import AbstractRepository, AbstractUnitOfWork
from app.modules.projects.domain.testing.fake_repository import FakeRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    project: FakeRepository
    committed = False

    def __init__(self, repository: AbstractRepository):
        self.project = repository

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
