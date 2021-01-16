from datetime import date
from typing import Optional

from todos.domain.models import Task


def build_task(
    *,
    name: str,
    id: Optional[int] = None,
    completed_at: [date] = None,
) -> Task:
    task = Task(name=name, completed_at=completed_at)
    task.id = id

    return task
