from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.application.testing.fake_project_repository import FakeProjectRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    project: FakeProjectRepository
    committed = False

    def __init__(self, repository: FakeProjectRepository):
        self.project = repository

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
