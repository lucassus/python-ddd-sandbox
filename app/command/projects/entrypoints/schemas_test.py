import json
from datetime import datetime

from app.query.schemas import Task


def test_task_schema_serialize():
    task = Task(number=1, name="Test")

    assert task.dict(by_alias=True) == dict(
        number=1,
        name="Test",
        completedAt=None,
    )


def test_task_schema_deserialize():
    task = Task.parse_raw(
        json.dumps(
            dict(
                number=2,
                name="Test 2",
                completedAt="2021-01-18T23:58:00",
            )
        )
    )

    assert task
    assert task.number == 2
    assert task.name == "Test 2"
    assert task.completed_at == datetime(2021, 1, 18, 23, 58, 0)
