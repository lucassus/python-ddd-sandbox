from todos.domain.models.task import Task
from todos.interfaces.fake_repository import FakeRepository


def test_fake_repository():
    repository = FakeRepository([])

    repository.create(Task(name="Foo"))
    repository.create(Task(name="Bar"))

    assert repository.list() == [Task(id=1, name="Foo"), Task(id=2, name="Bar")]
    assert repository.get(1) == Task(id=1, name="Foo")

    todo = repository.get(2)
    assert todo == Task(id=2, name="Bar")

    assert repository.get(123) is None
