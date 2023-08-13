import json

from app.command.projects.entrypoints.schemas import Task
from app.utc_datetime import utc_datetime


def test_task_schema_serialize():
    task = Task(number=1, name="Test")

    assert task.model_dump(by_alias=True) == {
        "number": 1,
        "name": "Test",
        "completedAt": None,
    }


def test_task_schema_deserialize():
    task = Task.model_validate_json(
        json.dumps(
            {
                "number": 2,
                "name": "Test 2",
                "completedAt": "2021-01-18T23:58:00Z",
            }
        )
    )

    assert task
    assert task.number == 2
    assert task.name == "Test 2"
    assert task.completed_at == utc_datetime(2021, 1, 18, 23, 58, 0)
