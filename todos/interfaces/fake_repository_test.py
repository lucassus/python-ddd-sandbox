from todos.domain.models import Task
from todos.interfaces.fake_repository import FakeRepository


def test_fake_repository():
    repository = FakeRepository(tasks=[])

    repository.create(Task(name="Foo"))
    repository.create(Task(name="Bar"))

    assert repository.list() == [
        repository.get(1),
        repository.get(2),
    ]

    assert repository.get(123) is None
