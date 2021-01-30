from datetime import date

from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

from app.modules.projects.domain.service import Service
from app.modules.projects.entrypoints import schemas
from app.modules.projects.entrypoints.dependencies import get_current_time, get_service

router = APIRouter()


@router.post("")
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    service: Service = Depends(get_service),
):
    task_id = service.create_task(name=data.name, project_id=project_id)

    return RedirectResponse(
        f"/projects/{project_id}/tasks/{task_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{id}/complete")
def task_complete_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task to complete", ge=1),
    service: Service = Depends(get_service),
    now: date = Depends(get_current_time),
):
    service.complete_task(id, project_id=project_id, now=now)

    return RedirectResponse(
        f"/projects/{project_id}/tasks/{id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{id}/incomplete")
def task_incomplete_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task to incomplete", ge=1),
    service: Service = Depends(get_service),
):
    service.incomplete_task(id, project_id=project_id)

    return RedirectResponse(
        f"/projects/{project_id}/tasks/{id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
