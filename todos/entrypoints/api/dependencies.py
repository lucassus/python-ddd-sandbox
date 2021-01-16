from fastapi import Depends

from todos.domain.models import Task
from todos.interfaces.db.unit_of_work import UnitOfWork
from todos.service_layer import services


def get_uow():
    with UnitOfWork() as uow:
        yield uow


class CreateTaskHandler:
    def __init__(self, uow=Depends(get_uow)):
        self._uow = uow

    def __call__(self, name: str) -> Task:
        return services.create_task(name, uow=self._uow)


class CompleteTaskHandler:
    def __init__(self, uow=Depends(get_uow)):
        self._uow = uow

    def __call__(self, task: Task) -> Task:
        return services.complete_task(task, uow=self._uow)


class IncompleteTaskHandler:
    def __init__(self, uow=Depends(get_uow)):
        self._uow = uow

    def __call__(self, task: Task) -> Task:
        return services.incomplete_task(task, uow=self._uow)
