from app.modules.projects.use_cases.ports import AbstractUnitOfWork
from app.modules.projects.use_cases.testing.fake_repository import FakeRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    project: FakeRepository
    committed = False

    def __init__(self, repository: FakeRepository):
        self.project = repository

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
