# TODO: Add ProjectNotFoundError and base EntityNotFoundError
# TODO: Add common api errors handler for such exceptions


class TaskNotFoundError(Exception):
    pass


class MaxIncompleteTasksNumberIsReached(Exception):
    pass
