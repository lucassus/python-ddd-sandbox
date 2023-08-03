from typing import TYPE_CHECKING

from app.command.projects.entities.errors import ArchiveProjectError, MaxIncompleteTasksNumberIsReached

if TYPE_CHECKING:
    from app.command.projects.entities.project import Project


def project_has_allowed_number_of_incomplete_tasks(project: "Project") -> None:
    if project.maximum_number_of_incomplete_tasks is None:
        return

    incomplete_tasks_number = len([task for task in project.tasks if not task.is_completed])

    if incomplete_tasks_number >= project.maximum_number_of_incomplete_tasks:
        raise MaxIncompleteTasksNumberIsReached


def can_archive(project: "Project") -> None:
    if project.incomplete_tasks_count > 0:
        raise ArchiveProjectError(
            f"Unable to archive project id={project.id}, "
            f"because it has {project.incomplete_tasks_count} incomplete tasks"
        )
