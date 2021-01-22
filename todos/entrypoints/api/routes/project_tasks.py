from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import RedirectResponse

from todos.domain.entities import Project
from todos.domain.service import Service
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import (
    get_current_time,
    get_project,
    get_service,
)

router = APIRouter()


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks")
def tasks_endpoint(project: Project = Depends(get_project)):
    return project.tasks


@router.post("", response_model=schemas.Task)
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    service: Service = Depends(get_service),
):
    task = service.create_task(data.name)

    # TODO: Almost works, find a way to redirect from POST to GET
    # TODO:
    return RedirectResponse(
        url=f"/projects/{project_id}/tasks/{task.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/{id}", response_model=schemas.Task)
def task_endpoint(
    project: Project = Depends(get_project),
    id: int = Path(..., description="The ID of the task", ge=1),
):
    return project.get_task(id)


@router.put("/{id}/complete", response_model=schemas.Task)
def task_complete_endpoint(
    id: int = Path(..., description="The ID of the task", ge=1),
    service: Service = Depends(get_service),
    now: date = Depends(get_current_time),
):
    return service.complete_task(id, now=now)


@router.put("/{id}/incomplete", response_model=schemas.Task)
def task_incomplete_endpoint(
    id: int = Path(..., description="The ID of the task", ge=1),
    service: Service = Depends(get_service),
):
    return service.incomplete_task(id)
