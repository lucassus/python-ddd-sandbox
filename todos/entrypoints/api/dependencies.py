from fastapi import Depends
from sqlalchemy.orm import Session

from todos.domain.models.todo import Todo
from todos.interfaces.abstract_repository import AbstractRepository
from todos.interfaces.db.repository import Repository
from todos.interfaces.db.session import SessionLocal
from todos.service_layer import services


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


class CreateTodoHandler:
    def __init__(
        self,
        session: Session = Depends(get_session),
        repository: AbstractRepository = Depends(get_repository),
    ):
        self._session = session
        self._repository = repository

    def __call__(self, name: str) -> Todo:
        return services.create_todo(
            name, session=self._session, repository=self._repository
        )


class CompleteTodoHandler:
    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def __call__(self, todo: Todo) -> Todo:
        return services.complete_todo(todo, session=self._session)


class IncompleteTodoHandler:
    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def __call__(self, todo: Todo) -> Todo:
        return services.incomplete_todo(todo, session=self._session)
