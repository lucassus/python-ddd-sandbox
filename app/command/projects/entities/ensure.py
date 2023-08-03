from typing import TYPE_CHECKING

from app.command.projects.entities.errors import (
    MaxIncompleteTasksNumberIsReachedError,
    ProjectIsNotCompletedError,
    ProjectNotArchivedError,
)

if TYPE_CHECKING:
    from app.command.projects.entities.project import Project


def project_has_allowed_number_of_incomplete_tasks(project: "Project") -> None:
    if project.maximum_number_of_incomplete_tasks is None:
        return

    if project.incomplete_tasks_count >= project.maximum_number_of_incomplete_tasks:
        raise MaxIncompleteTasksNumberIsReachedError()


def all_project_tasks_are_completed(project: "Project") -> None:
    if project.incomplete_tasks_count > 0:
        raise ProjectIsNotCompletedError(f"Project has {project.incomplete_tasks_count} incomplete tasks")


def project_is_archived(project: "Project") -> None:
    if not project.archived:
        raise ProjectNotArchivedError()
