from app.shared_kernel.errors import EntityNotFoundError


class ProjectNotFoundError(EntityNotFoundError):
    def __init__(self, id: int):
        self.message = f"Unable to find a project with id={id}"


class TaskNotFoundError(EntityNotFoundError):
    def __init__(self, id: int):
        self.message = f"Unable to find a task with id={id}"


class MaxIncompleteTasksNumberIsReached(Exception):
    pass
