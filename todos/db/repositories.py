import abc
from datetime import date
from typing import List, Optional

from sqlalchemy.orm.session import Session

from todos.domain.models import Todo


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> Optional[Todo]:
        ...

    @abc.abstractmethod
    def list(self) -> List[Todo]:
        ...

    @abc.abstractmethod
    def update(self, todo: Todo, completed_at: Optional[date]) -> Todo:
        ...

    @abc.abstractmethod
    def create(self, name: str) -> Todo:
        ...


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
        self._session.commit()

        return todo

    def update(self, todo: Todo, completed_at: Optional[date]) -> Todo:
        todo.completed_at = completed_at
        self._session.commit()

        return todo


class FakeRepository(AbstractRepository):
    def __init__(self, todos: List[Todo]):
        self._todos = todos

    def get(self, id: int) -> Optional[Todo]:
        try:
            return next(todo for todo in self._todos if todo.id == id)
        except StopIteration:
            return None

    def create(self, name: str) -> Todo:
        todo = Todo(id=self._next_id, name=name)
        self._todos.append(todo)

        return todo

    def update(self, todo: Todo, completed_at: Optional[date]) -> Todo:
        todo.completed_at = completed_at
        return todo

    def list(self) -> List[Todo]:
        return self._todos

    @property
    def _next_id(self) -> int:
        return (
            max(todo.id for todo in self._todos if todo.id) + 1
            if len(self._todos) > 0
            else 1
        )
