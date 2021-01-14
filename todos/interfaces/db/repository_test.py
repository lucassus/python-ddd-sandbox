from todos.domain.models.task import Task
from todos.interfaces.db.repository import Repository


def test_repository_get(session):
    todo = Task(name="Test todo")
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

    todo = Task(name="One")
    session.add(todo)

    todo = Task(name="Two")
    session.add(todo)

    session.commit()

    assert len(repository.list()) == 2
