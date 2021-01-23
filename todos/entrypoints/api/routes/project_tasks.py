from datetime import date

from fastapi import APIRouter, Depends, Path, Request, status
from fastapi.responses import RedirectResponse

from todos.domain.service import Service
from todos.entrypoints.api import schemas
from todos.entrypoints.api.dependencies import get_current_time, get_service

router = APIRouter()


@router.post("")
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    request: Request,
    service: Service = Depends(get_service),
):
    task_id = service.create_task(data.name)

    return RedirectResponse(
        url=request.url_for("task_endpoint", project_id=project_id, id=task_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{id}/complete")
def task_complete_endpoint(
    request: Request,
    project_id: int,
    id: int = Path(..., description="The ID of the task", ge=1),
    service: Service = Depends(get_service),
    now: date = Depends(get_current_time),
):
    service.complete_task(id, project_id=project_id, now=now)

    return RedirectResponse(
        url=request.url_for("task_endpoint", project_id=project_id, id=id),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{id}/incomplete")
def task_incomplete_endpoint(
    request: Request,
    project_id: int,
    id: int = Path(..., description="The ID of the task", ge=1),
    service: Service = Depends(get_service),
):
    service.incomplete_task(id, project_id=project_id)

    # TODO: Figure out how to dry it
    return RedirectResponse(
        url=request.url_for("task_endpoint", project_id=project_id, id=id),
        status_code=status.HTTP_303_SEE_OTHER,
    )
