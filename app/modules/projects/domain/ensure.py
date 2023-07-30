from typing import TYPE_CHECKING

from app.modules.projects.domain.errors import MaxIncompleteTasksNumberIsReached

if TYPE_CHECKING:
    from app.modules.projects.domain.project import Project


def project_has_allowed_number_of_incomplete_tasks(project: "Project") -> None:
    if project.maximum_number_of_incomplete_tasks is None:
        return

    incomplete_tasks_number = len([task for task in project.tasks if not task.is_completed])

    if incomplete_tasks_number >= project.maximum_number_of_incomplete_tasks:
        raise MaxIncompleteTasksNumberIsReached
