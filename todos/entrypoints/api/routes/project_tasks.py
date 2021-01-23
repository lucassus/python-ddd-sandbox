from datetime import date

from fastapi import APIRouter, Depends, Path

from todos.domain.service import Service
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import (
    get_current_time,
    get_service,
    SeeOtherRedirect,
)

router = APIRouter()


@router.post("")
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    service: Service = Depends(get_service),
    see_other: SeeOtherRedirect = Depends(),
):
    task_id = service.create_task(name=data.name, project_id=project_id)
    return see_other("task_endpoint", project_id=project_id, id=task_id)


@router.put("/{id}/complete")
def task_complete_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task to complete", ge=1),
    service: Service = Depends(get_service),
    now: date = Depends(get_current_time),
    see_other: SeeOtherRedirect = Depends(),
):
    service.complete_task(id, project_id=project_id, now=now)
    return see_other("task_endpoint", project_id=project_id, id=id)


@router.put("/{id}/incomplete")
def task_incomplete_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task to incomplete", ge=1),
    service: Service = Depends(get_service),
    see_other: SeeOtherRedirect = Depends(),
):
    service.incomplete_task(id, project_id=project_id)
    return see_other("task_endpoint", project_id=project_id, id=id)
