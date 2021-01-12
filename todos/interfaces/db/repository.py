from typing import List, Optional

from sqlalchemy.orm.session import Session

from todos.domain.models.todo import Todo
from todos.interfaces.abstract_repository import AbstractRepository


class Repository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def get(self, id: int) -> Optional[Todo]:
        return self._session.query(Todo).get(id)

    def list(self) -> List[Todo]:
        return self._session.query(Todo).all()

    def create(self, todo: Todo) -> None:
        self._session.add(todo)
