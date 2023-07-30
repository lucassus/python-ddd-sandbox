from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

from app.modules.projects.domain.entities import TaskNumber
from app.modules.projects.domain.entities.project import ProjectID
from app.modules.projects.domain.use_cases import CreateProject
from app.modules.projects.domain.use_cases.tasks_service import TasksService
from app.modules.projects.entrypoints import schemas
from app.modules.projects.entrypoints.dependencies import get_create_project, get_current_time, get_tasks_service
from app.shared_kernel.user_id import UserID

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("")
def project_create_endpoint(
    data: schemas.CreateProject,
    create_project: Annotated[CreateProject, Depends(get_create_project)],
):
    project_id = create_project(
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
    service: Annotated[TasksService, Depends(get_tasks_service)],
):
    task_number = service.create_task(
        project_id=ProjectID(project_id),
        name=data.name,
    )

    return RedirectResponse(
        f"/queries/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{project_id}/tasks/{number}/complete")
def task_complete_endpoint(
    project_id: int,
    service: Annotated[TasksService, Depends(get_tasks_service)],
    now: Annotated[date, Depends(get_current_time)],
    number: int = Path(..., description="The number of the task to complete", ge=1),
):
    service.complete_task(TaskNumber(number), project_id=ProjectID(project_id), now=now)

    return RedirectResponse(
        f"/queries/projects/{project_id}/tasks/{number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{project_id}/tasks/{number}/incomplete")
def task_incomplete_endpoint(
    project_id: int,
    service: Annotated[TasksService, Depends(get_tasks_service)],
    number: int = Path(..., description="The number of the task to incomplete", ge=1),
):
    service.incomplete_task(TaskNumber(number), project_id=ProjectID(project_id))

    return RedirectResponse(
        f"/queries/projects/{project_id}/tasks/{number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
