from app.modules.accounts.domain.ports import AbstractRepository, AbstractUnitOfWork


# TODO: Backport this change to projects module
class FakeUnitOfWork(AbstractUnitOfWork):
    repository: AbstractRepository
    committed = False

    def __init__(self, repository: AbstractRepository):
        self._repository_factory = lambda: repository

    def __enter__(self):
        self.repository = self._repository_factory()
        return super().__enter__()

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
