from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

from app.modules.projects.domain.entities import TaskID
from app.modules.projects.domain.entities.project import ProjectID
from app.modules.projects.domain.service import Service
from app.modules.projects.entrypoints import schemas
from app.modules.projects.entrypoints.dependencies import get_current_time, get_service
from app.shared_kernel.user_id import UserID

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("")
def project_create_endpoint(
    data: schemas.CreateProject,
    service: Annotated[Service, Depends(get_service)],
):
    project_id = service.create_project(
        user_id=UserID(data.user_id),
        name=data.name,
    )

    return RedirectResponse(
        f"/queries/projects/{project_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/{project_id}/tasks")
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    service: Annotated[Service, Depends(get_service)],
):
    task_id = service.create_task(name=data.name, project_id=ProjectID(project_id))

    return RedirectResponse(
        f"/projects/{project_id}/tasks/{task_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{project_id}/tasks/{id}/complete")
def task_complete_endpoint(
    project_id: int,
    service: Annotated[Service, Depends(get_service)],
    now: Annotated[date, Depends(get_current_time)],
    id: int = Path(..., description="The ID of the task to complete", ge=1),
):
    service.complete_task(TaskID(id), project_id=ProjectID(project_id), now=now)

    return RedirectResponse(
        f"/projects/{project_id}/tasks/{id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{project_id}/tasks/{id}/incomplete")
def task_incomplete_endpoint(
    project_id: int,
    service: Annotated[Service, Depends(get_service)],
    id: int = Path(..., description="The ID of the task to incomplete", ge=1),
):
    service.incomplete_task(TaskID(id), project_id=ProjectID(project_id))

    return RedirectResponse(
        f"/projects/{project_id}/tasks/{id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
