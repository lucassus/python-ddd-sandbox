from typing import TYPE_CHECKING

from todos.domain.errors import MaxUnfinishedTasksNumberIfReached

if TYPE_CHECKING:
    from todos.domain.entities import Project


def max_unfinished_tasks_number_is_not_reached(project: "Project") -> None:
    if project.max_unfinished_tasks_number is None:
        return

    unfinished_tasks = [task for task in project.tasks if not task.is_completed]

    if len(unfinished_tasks) >= project.max_unfinished_tasks_number:
        raise MaxUnfinishedTasksNumberIfReached
