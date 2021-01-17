from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork
from todos.interfaces.db.repository import Repository
from todos.interfaces.db.session import SessionLocal


class UnitOfWork(AbstractUnitOfWork):
    repository: Repository

    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def __enter__(self):
        self._session = self._session_factory()
        self.repository = Repository(session=self._session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
