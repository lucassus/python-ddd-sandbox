from datetime import date
from typing import Optional

from app.modules.projects.domain.entities import Project, ProjectID, Task, TaskID


def build_project(
    *,
    id: Optional[ProjectID] = None,
    name: str = "Test project",
    maximum_number_of_incomplete_tasks: Optional[int] = None,
) -> Project:
    project = Project(
        name=name,
        maximum_number_of_incomplete_tasks=maximum_number_of_incomplete_tasks,
    )

    if id is not None:
        project.id = id

    return project


def build_task(
    *,
    id: Optional[TaskID] = None,
    name: str = "Test task",
    completed_at: Optional[date] = None,
) -> Task:
    task = Task(name=name, completed_at=completed_at)

    if id is not None:
        task.id = id

    return task
