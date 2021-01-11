from datetime import date
from typing import List, Optional

from sqlalchemy.orm.session import Session

from todos.db.abstract_repository import AbstractRepository
from todos.domain.models import Todo


class Repository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def get(self, id: int) -> Optional[Todo]:
        return self._session.query(Todo).get(id)

    def list(self) -> List[Todo]:
        return self._session.query(Todo).all()

    def create(self, name: str) -> Todo:
        todo = Todo(name=name)
        self._session.add(todo)

        return todo

    def update(
        self, id: int, name: Optional[str] = None, completed_at: Optional[date] = ...
    ) -> Todo:
        todo = self.get(id)
        assert todo is not None

        if name is not None:
            todo.name = name

        if completed_at is not ...:
            todo.completed_at = completed_at

        return todo
