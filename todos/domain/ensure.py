from typing import TYPE_CHECKING

from todos.domain.errors import MaximumNumberOfUnfinishedTasksIfReached

if TYPE_CHECKING:
    from todos.domain.entities import Project


def allowed_number_of_unfinished_tasks_is_not_reached(project: "Project") -> None:
    if project.allowed_number_of_unfinished_tasks is None:
        return

    unfinished_tasks = [task for task in project.tasks if not task.is_completed]

    if len(unfinished_tasks) >= project.allowed_number_of_unfinished_tasks:
        raise MaximumNumberOfUnfinishedTasksIfReached
