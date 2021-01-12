from fastapi import Depends
from sqlalchemy.orm import Session

from todos.domain.models.todo import Todo
from todos.interfaces.abstract_repository import AbstractRepository
from todos.interfaces.db.repository import Repository
from todos.interfaces.db.session import SessionLocal
from todos.service_layer.services import complete_todo, create_todo, incomplete_todo


def get_session():
    session = SessionLocal()

    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()


def get_repository(session: Session = Depends(get_session)) -> AbstractRepository:
    return Repository(session=session)


class Service:
    def __init__(self, session: Session = Depends(get_session)):
        self._session = session
        self._repository = Repository(session=session)

    def create_todo(self, name: str) -> Todo:
        return create_todo(
            name,
            repository=self._repository,
            session=self._session,
        )

    def complete_todo(self, id: int) -> Todo:
        return complete_todo(
            id,
            repository=self._repository,
            session=self._session,
        )

    def incomplete_todo(self, id: int) -> Todo:
        return incomplete_todo(
            id,
            repository=self._repository,
            session=self._session,
        )
