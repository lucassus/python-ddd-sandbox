from todos.entrypoints.api.schemas import Task


def test_task_schema():
    todo = Task(id=1, name="Test")
    assert todo.dict(by_alias=True) == {
        "id": 1,
        "name": "Test",
        "completedAt": None,
    }
