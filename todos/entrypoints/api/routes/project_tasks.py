from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Path

from todos.domain.entities import Project
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import get_current_time, get_project, get_uow
from todos.service_layer import services
from todos.service_layer.abstract_unit_of_work import AbstractUnitOfWork

router = APIRouter()


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks")
def tasks_endpoint(project: Project = Depends(get_project)):
    return project.tasks


@router.post("", response_model=schemas.Task)
def task_create_endpoint(
    data: schemas.CreateTask,
    project: Project = Depends(get_project),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    return services.create_task(data.name, project=project, uow=uow)


@router.get("/{id}", response_model=schemas.Task)
def task_endpoint(
    project: Project = Depends(get_project),
    id: int = Path(..., description="The ID of the task", ge=1),
):
    return project.get_task(id)


@router.put("/{id}/complete", response_model=schemas.Task)
def task_complete_endpoint(
    id: int = Path(..., description="The ID of the task", ge=1),
    project: Project = Depends(get_project),
    uow: AbstractUnitOfWork = Depends(get_uow),
    now: date = Depends(get_current_time),
):
    return services.complete_task(id, project=project, now=now, uow=uow)


@router.put("/{id}/incomplete", response_model=schemas.Task)
def task_incomplete_endpoint(
    id: int = Path(..., description="The ID of the task", ge=1),
    project: Project = Depends(get_project),
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    return services.incomplete_task(id, project=project, uow=uow)
