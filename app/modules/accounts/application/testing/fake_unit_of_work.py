from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.application.ports.tracking_user_repository import TrackingUserRepository
from app.shared.message_bus import SupportsDispatchingEvents


class FakeUnitOfWork(AbstractUnitOfWork):
    committed = False

    def __init__(self, repository: TrackingUserRepository, bus: SupportsDispatchingEvents):
        super().__init__(bus=bus)
        self._repository_factory = lambda: repository

    def __enter__(self):
        self.users = self._repository_factory()
        return super().__enter__()

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass
