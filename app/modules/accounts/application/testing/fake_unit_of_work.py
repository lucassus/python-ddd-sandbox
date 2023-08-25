from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.application.testing.fake_user_repository import FakeUserRepository
from app.modules.shared_kernel.message_bus import SupportsDispatch


class FakeUnitOfWork(AbstractUnitOfWork):
    committed = False

    def __init__(self, repository: FakeUserRepository, bus: SupportsDispatch):
        super().__init__(bus=bus)
        self._repository_factory = lambda: repository

    def __enter__(self):
        self.users = self._repository_factory()
        return super().__enter__()

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass
