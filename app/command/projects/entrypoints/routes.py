from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

from app.command.projects.application.create_project import CreateProject
from app.command.projects.application.tasks_service import TasksService
from app.command.projects.entities.project import ProjectID
from app.command.projects.entities.task import TaskNumber
from app.command.projects.entrypoints import schemas
from app.command.projects.entrypoints.dependencies import get_create_project, get_current_time, get_tasks_service
from app.shared_kernel.user_id import UserID

# TODO: Split there routes into separate files, projects, for example project_tasks
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


@router.put("/{project_id}/tasks/{task_number}/complete")
def task_complete_endpoint(
    project_id: int,
    service: Annotated[TasksService, Depends(get_tasks_service)],
    now: Annotated[date, Depends(get_current_time)],
    task_number: int = Path(..., description="The number of the task to complete", ge=1),
):
    service.complete_task(
        TaskNumber(task_number),
        project_id=ProjectID(project_id),
        now=now,
    )

    return RedirectResponse(
        f"/queries/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{project_id}/tasks/{task_number}/incomplete")
def task_incomplete_endpoint(
    project_id: int,
    service: Annotated[TasksService, Depends(get_tasks_service)],
    task_number: int = Path(..., description="The number of the task to incomplete", ge=1),
):
    service.incomplete_task(
        TaskNumber(task_number),
        project_id=ProjectID(project_id),
    )

    return RedirectResponse(
        f"/queries/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
