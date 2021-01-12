from datetime import date

from todos.db.fake_repository import FakeRepository
from todos.domain.models.todo import Todo
from todos.service_layer.services import complete_todo, incomplete_todo


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_complete():
    # Given
    todo = Todo(id=1, name="Test todo")
    fake_repository = FakeRepository([todo])
    fake_session = FakeSession()

    # When
    now = date(2021, 1, 8)
    assert todo.id is not None
    completed_todo = complete_todo(
        todo.id, now=lambda: now, repository=fake_repository, session=fake_session
    )

    # Then
    assert completed_todo == todo
    assert completed_todo.completed_at is now
    assert fake_session.committed


def test_incomplete():
    # Given
    todo = Todo(id=1, name="Test todo", completed_at=date(2021, 1, 5))
    fake_repository = FakeRepository([todo])
    fake_session = FakeSession()

    # When
    assert todo.id is not None
    completed_todo = incomplete_todo(
        todo.id, repository=fake_repository, session=fake_session
    )

    # Then
    assert completed_todo == todo
    assert completed_todo.completed_at is None
    assert fake_session.committed
