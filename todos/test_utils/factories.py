from datetime import date
from typing import Optional

from todos.domain.models import Project, Task


def build_project(
    *,
    name: Optional[str] = "Test project",
    id: Optional[int] = None,
) -> Project:
    project = Project(name=name)
    project.id = id

    return project


def build_task(
    *,
    name: Optional[str] = "Test task",
    id: Optional[int] = None,
    completed_at: [date] = None,
) -> Task:
    task = Task(name=name, completed_at=completed_at)
    task.id = id

    return task
