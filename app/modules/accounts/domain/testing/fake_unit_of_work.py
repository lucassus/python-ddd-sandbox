from app.modules.accounts.domain.ports import AbstractRepository, AbstractUnitOfWork


class FakeUnitOfWork(AbstractUnitOfWork):
    committed = False

    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
