from app.modules.accounts.domain.ports import AbstractRepository, AbstractUnitOfWork


class FakeUnitOfWork(AbstractUnitOfWork):
    user: AbstractRepository
    committed = False

    def __init__(self, repository: AbstractRepository):
        self._repository_factory = lambda: repository

    def __enter__(self):
        self.user = self._repository_factory()
        return super().__enter__()

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
