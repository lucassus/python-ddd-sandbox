from typing import TYPE_CHECKING

from app.command.shared_kernel.errors import EntityNotFoundError

if TYPE_CHECKING:
    from app.command.projects.entities.project import ProjectID, TaskNumber


class ProjectNotFoundError(EntityNotFoundError):
    def __init__(self, id: "ProjectID"):
        super().__init__(f"Unable to find Project with {id=}")


class TaskNotFoundError(EntityNotFoundError):
    def __init__(self, number: "TaskNumber"):
        super().__init__(f"Unable to find Task with {number=}")


class ProjectStateError(Exception):
    pass


class MaxIncompleteTasksNumberIsReachedError(ProjectStateError):
    pass


class ProjectIsNotCompletedError(ProjectStateError):
    pass


class ProjectNotArchivedError(ProjectStateError):
    pass
