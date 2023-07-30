from typing import TYPE_CHECKING

from app.shared_kernel.errors import EntityNotFoundError

if TYPE_CHECKING:
    from app.modules.projects.domain.entities import ProjectID, TaskNumber


class ProjectNotFoundError(EntityNotFoundError):
    def __init__(self, id: "ProjectID"):
        super().__init__(f"Unable to find Project with {id=}")


class TaskNotFoundError(EntityNotFoundError):
    def __init__(self, number: "TaskNumber"):
        super().__init__(f"Unable to find Task with {number=}")


class MaxIncompleteTasksNumberIsReached(Exception):
    pass
