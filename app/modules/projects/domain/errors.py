from typing import TYPE_CHECKING

from app.shared_kernel.errors import EntityNotFoundError

if TYPE_CHECKING:
    from app.modules.projects.domain.entities import ProjectID, TaskID


class ProjectNotFoundError(EntityNotFoundError):
    def __init__(self, id: "ProjectID"):
        self.message = f"Unable to find a project with {id=}"


class TaskNotFoundError(EntityNotFoundError):
    def __init__(self, id: "TaskID"):
        self.message = f"Unable to find a task with {id=}"


class MaxIncompleteTasksNumberIsReached(Exception):
    pass
