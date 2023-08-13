from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    user: AbstractUserRepository
    committed = False

    def __init__(self, repository: AbstractUserRepository):
        self._repository_factory = lambda: repository

    def __enter__(self):
        self.user = self._repository_factory()
        return super().__enter__()

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
