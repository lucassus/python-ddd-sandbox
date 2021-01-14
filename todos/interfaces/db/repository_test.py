from todos.domain.models import Task
from todos.interfaces.db.repository import Repository


def test_repository_get(session):
    task = Task(name="Test task")
    session.add(task)
    session.commit()

    repository = Repository(session=session)
    assert repository.get(1) == task


def test_repository_get_returns_none(session):
    repository = Repository(session=session)
    assert repository.get(1) is None


def test_repository_list(session):
    repository = Repository(session=session)

    assert repository.list() == []

    task = Task(name="One")
    session.add(task)

    task = Task(name="Two")
    session.add(task)

    session.commit()

    assert len(repository.list()) == 2
