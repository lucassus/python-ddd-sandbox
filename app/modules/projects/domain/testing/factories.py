from datetime import date
from typing import Optional

from app.modules.projects.domain.entities import Task, TaskID


# TODO: Find a better solution for this, it leaks id, which is db's implementation detail
def build_test_task(
    *,
    id: Optional[TaskID] = None,
    name: str = "Test task",
    completed_at: Optional[date] = None,
) -> Task:
    task = Task(name=name, completed_at=completed_at)

    if id is not None:
        task.id = id

    return task
