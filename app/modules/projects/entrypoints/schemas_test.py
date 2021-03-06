import json
from datetime import date

from app.query.schemas import Task


def test_task_schema_serialize():
    task = Task(id=1, name="Test")

    assert task.dict(by_alias=True) == dict(
        id=1,
        name="Test",
        completedAt=None,
    )


def test_task_schema_deserialize():
    task = Task.parse_raw(
        json.dumps(
            dict(
                id=2,
                name="Test 2",
                completedAt="2021-01-18",
            )
        )
    )

    assert task
    assert task.id == 2
    assert task.name == "Test 2"
    assert task.completed_at == date(2021, 1, 18)
