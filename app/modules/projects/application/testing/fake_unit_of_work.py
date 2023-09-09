from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.shared.message_bus import SupportsDispatchingEvents


class FakeUnitOfWork(AbstractUnitOfWork):
    projects: FakeProjectRepository
    committed = False

    def __init__(self, repository: FakeProjectRepository, bus: SupportsDispatchingEvents):
        super().__init__(bus)
        self.projects = repository

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass
