from typing import TYPE_CHECKING

from app.modules.shared_kernel.errors import EntityNotFoundError

if TYPE_CHECKING:
    from app.modules.projects.domain.project import ProjectID
    from app.modules.projects.domain.task import TaskNumber


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
