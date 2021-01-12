from datetime import date

from todos.db.abstract_repository import AbstractRepository
from todos.db.repository import Repository
from todos.domain.models import Todo


def test_repository_get(session):
    todo = Todo(name="Test todo")
    session.add(todo)
    session.commit()

    repository = Repository(session=session)
    assert repository.get(1) == todo


def test_repository_get_returns_none(session):
    repository = Repository(session=session)
    assert repository.get(1) is None


def test_repository_list(session):
    repository = Repository(session=session)

    assert repository.list() == []

    todo = Todo(name="One")
    session.add(todo)

    todo = Todo(name="Two")
    session.add(todo)

    session.commit()

    assert len(repository.list()) == 2


def test_repository_update_completed_at(session):
    repository = Repository(session=session)

    todo = Todo(name="One")
    session.add(todo)
    session.commit()

    assert todo.id is not None
    repository.update(todo.id, completed_at=date(2021, 1, 6))
    updated_todo = session.query(Todo).get(todo.id)

    assert updated_todo.completed_at is not None

    repository.update(updated_todo.id, completed_at=None)
    assert updated_todo.completed_at is None


def test_repository_update_name(session):
    repository = Repository(session=session)

    todo = Todo(name="One", completed_at=date(2021, 1, 6))
    session.add(todo)
    session.commit()

    assert todo.id is not None
    repository.update(todo.id, name="Two")
    updated_todo = session.query(Todo).get(todo.id)

    assert updated_todo.completed_at is not None
    assert updated_todo.name == "Two"
