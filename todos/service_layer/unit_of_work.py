from typing import Optional

from sqlalchemy.orm import Session

from todos.interfaces.db.repository import Repository
from todos.interfaces.db.session import SessionLocal
from todos.service_layer.abstract_unit_of_work import AbstractUnitOfWork


# TODO: See https://github.com/cosmicpython/code/issues/23
# TODO: http://io.made.com/blog/2017-09-08-repository-and-unit-of-work-pattern-in-python.html
# TODO: Inject the session and start the nested transaction
#  https://docs.sqlalchemy.org/en/13/orm/session_transaction.html#using-savepoint
class UnitOfWork(AbstractUnitOfWork):
    _session: Optional[Session]

    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def __enter__(self):
        self._session = self._session_factory(expire_on_commit=False)
        # self._session.expire_on_commit = False

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    @property
    def repository(self) -> Repository:
        return Repository(session=self._session)

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
