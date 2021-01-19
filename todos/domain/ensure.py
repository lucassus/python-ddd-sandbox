from typing import TYPE_CHECKING

from todos.domain.errors import MaxIncompleteTasksNumberIsReached

if TYPE_CHECKING:
    from todos.domain.entities import Project


def max_incomplete_tasks_number_is_not_reached(project: "Project") -> None:
    if project.max_incomplete_tasks_number is None:
        return

    incomplete_tasks_number = len(
        [task for task in project.tasks if not task.is_completed]
    )

    if incomplete_tasks_number >= project.max_incomplete_tasks_number:
        raise MaxIncompleteTasksNumberIsReached
