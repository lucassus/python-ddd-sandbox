from datetime import date

from todos.domain.models import Task
from todos.interfaces.fake_repository import FakeRepository
from todos.service_layer.services import complete_task, create_task, incomplete_task


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


# def test_create_task():
#     # Given
#     fake_session = FakeSession()
#     fake_repository = FakeRepository([])
#
#     task = create_task(
#         "Testing...",
#         session=fake_session,
#         repository=fake_repository,
#     )
#
#     assert task
#     assert task.id == 1
#     assert task.name == "Testing..."
#     assert fake_session.committed
#
#     assert fake_repository.get(1) == task


def test_complete():
    # Given
    task = Task(name="Test task")
    fake_session = FakeSession()

    # When
    now = date(2021, 1, 8)
    completed_task = complete_task(
        task,
        session=fake_session,
        now=lambda: now,
    )

    # Then
    assert completed_task == task
    assert completed_task.completed_at is now
    assert fake_session.committed


def test_incomplete():
    # Given
    task = Task(name="Test task", completed_at=date(2021, 1, 5))
    fake_session = FakeSession()

    # When
    completed_task = incomplete_task(
        task,
        session=fake_session,
    )

    # Then
    assert completed_task == task
    assert completed_task.completed_at is None
    assert fake_session.committed
