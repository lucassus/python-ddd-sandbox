from typing import TYPE_CHECKING

from todos.services.project_management.domain.errors import (
    MaxIncompleteTasksNumberIsReached,
)

if TYPE_CHECKING:
    from todos.services.project_management.domain.entities import Project


def project_has_allowed_number_of_incomplete_tasks(project: "Project") -> None:
    if project.max_incomplete_tasks_number is None:
        return

    incomplete_tasks_number = len(
        [task for task in project.tasks if not task.is_completed]
    )

    if incomplete_tasks_number >= project.max_incomplete_tasks_number:
        raise MaxIncompleteTasksNumberIsReached
