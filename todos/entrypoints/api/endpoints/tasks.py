from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status

from todos.domain.models import Task
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import (
    CompleteTaskHandler,
    CreateTaskHandler,
    IncompleteTaskHandler,
    get_repository,
    get_uow,
)
from todos.interfaces.abstract_repository import AbstractRepository
from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork

router = APIRouter()


@router.get("", response_model=List[schemas.Task])
def tasks_endpoint(uof: AbstractUnitOfWork = Depends(get_uow)):
    return uof.repository.list()


@router.post("", response_model=schemas.Task)
def task_create_endpoint(
    data: schemas.CreateTask,
    create_task: CreateTaskHandler = Depends(),
):
    return create_task(name=data.name)


def get_task(
    id: int = Path(..., description="The ID of the task", ge=1),
    repository: AbstractRepository = Depends(get_repository),
) -> Task:
    task = repository.get(id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a task with ID={id}",
        )

    return task


@router.get("/{id}", response_model=schemas.Task)
def task_endpoint(task: Task = Depends(get_task)):
    return task


@router.put("/{id}/complete", response_model=schemas.Task)
def task_complete_endpoint(
    task: Task = Depends(get_task),
    complete_task: CompleteTaskHandler = Depends(),
):
    return complete_task(task)


@router.put("/{id}/incomplete", response_model=schemas.Task)
def task_incomplete_endpoint(
    task: Task = Depends(get_task),
    incomplete_task: IncompleteTaskHandler = Depends(),
):
    return incomplete_task(task)
