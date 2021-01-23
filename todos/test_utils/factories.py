from datetime import date
from typing import Optional

from todos.commands.domain.entities import Project, Task


def build_project(
    *,
    name: str = "Test project",
    id: Optional[int] = None,
    max_incomplete_tasks_number: Optional[int] = None,
) -> Project:
    project = Project(
        name=name,
        max_incomplete_tasks_number=max_incomplete_tasks_number,
    )

    if id is not None:
        project.id = id

    return project


def build_task(
    *,
    name: str = "Test task",
    id: Optional[int] = None,
    completed_at: Optional[date] = None,
) -> Task:
    task = Task(name=name, completed_at=completed_at)

    if id is not None:
        task.id = id

    return task
