from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status

from todos.domain.models import Project, Task
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


def get_project(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> Project:
    project = uow.repository.get()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a project",
        )

    return project


@router.get("/{id}", response_model=schemas.Task)
def task_endpoint(task: Task = Depends(get_project)):
    return task


@router.put("/{id}/complete", response_model=schemas.Task)
def task_complete_endpoint(
    project: Task = Depends(get_project),
    id: int = Path(..., description="The ID of the task", ge=1),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    task = services.complete_task(id=id, uow=uow)
    return task


@router.put("/{id}/incomplete", response_model=schemas.Task)
def task_incomplete_endpoint(
    project: Task = Depends(get_project),
    id: int = Path(..., description="The ID of the task", ge=1),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    task = services.incomplete_task(id=id, uow=uow)
    return task
