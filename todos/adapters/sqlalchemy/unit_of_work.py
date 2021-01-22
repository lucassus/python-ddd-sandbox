from sqlalchemy.orm import Session

from todos.adapters.sqlalchemy.repository import Repository
from todos.domain.ports import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    repository: Repository

    def __init__(self, session: Session):
        self._session = session

    def __enter__(self):
        self.repository = Repository(session=self._session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.rollback()  # It does nothing when the session has been committed before

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
