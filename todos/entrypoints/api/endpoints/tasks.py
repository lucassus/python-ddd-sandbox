from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status

from todos.domain.models import Task
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import get_uow
from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork
from todos.service_layer import services

router = APIRouter()


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks")
def tasks_endpoint(uow: AbstractUnitOfWork = Depends(get_uow)):
    project = uow.repository.get()
    return project.tasks


@router.post("", response_model=schemas.Task)
def task_create_endpoint(
    data: schemas.CreateTask,
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    task = services.create_task(name=data.name, uow=uow)
    return task


def get_task(
    id: int = Path(..., description="The ID of the task", ge=1),
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Task:
    task = uow.repository.get(id)

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
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    return services.complete_task(task, uow=uow)


@router.put("/{id}/incomplete", response_model=schemas.Task)
def task_incomplete_endpoint(
    task: Task = Depends(get_task),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    return services.incomplete_task(task, uow=uow)
