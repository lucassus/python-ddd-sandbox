from todos.factories import build_task
from todos.interfaces.fake_repository import FakeRepository


def test_fake_repository():
    repository = FakeRepository(
        tasks=[
            build_task(id=1, name="First"),
        ]
    )

    repository.create(build_task(name="Foo"))
    repository.create(build_task(name="Bar"))

    assert repository.list() == [
        repository.get(1),
        repository.get(2),
        repository.get(3),
    ]

    task = repository.get(1)
    assert task is not None
    assert task.id == 1

    assert repository.get(123) is None
