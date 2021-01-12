from todos.db.fake_repository import FakeRepository
from todos.domain.models.todo import Todo


def test_fake_repository():
    repository = FakeRepository([])

    repository.create("Foo")
    repository.create("Bar")

    assert repository.list() == [Todo(id=1, name="Foo"), Todo(id=2, name="Bar")]
    assert repository.get(1) == Todo(id=1, name="Foo")

    todo = repository.get(2)
    assert todo == Todo(id=2, name="Bar")

    assert repository.get(123) is None
