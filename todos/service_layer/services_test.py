from datetime import date

from todos.domain.models.task import Task
from todos.interfaces.fake_repository import FakeRepository
from todos.service_layer.services import complete_todo, create_todo, incomplete_todo


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_create_todo():
    # Given
    fake_session = FakeSession()
    fake_repository = FakeRepository([])

    todo = create_todo(
        "Testing...",
        session=fake_session,
        repository=fake_repository,
    )

    assert todo
    assert todo.id == 1
    assert todo.name == "Testing..."
    assert fake_session.committed

    assert fake_repository.get(1) == todo


def test_complete():
    # Given
    todo = Task(id=1, name="Test todo")
    fake_session = FakeSession()

    # When
    now = date(2021, 1, 8)
    completed_todo = complete_todo(
        todo,
        session=fake_session,
        now=lambda: now,
    )

    # Then
    assert completed_todo == todo
    assert completed_todo.completed_at is now
    assert fake_session.committed


def test_incomplete():
    # Given
    todo = Task(id=1, name="Test todo", completed_at=date(2021, 1, 5))
    fake_session = FakeSession()

    # When
    completed_todo = incomplete_todo(
        todo,
        session=fake_session,
    )

    # Then
    assert completed_todo == todo
    assert completed_todo.completed_at is None
    assert fake_session.committed
