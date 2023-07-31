from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

from app.command.projects.application.tasks_service import TasksService
from app.command.projects.entities.project import ProjectID
from app.command.projects.entities.task import TaskNumber
from app.command.projects.entrypoints import schemas
from app.command.projects.entrypoints.dependencies import get_current_time, get_tasks_service

router = APIRouter(prefix="/projects/{project_id}/tasks")


@router.post("")
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


@router.put("/{task_number}/complete")
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


@router.put("/{task_number}/incomplete")
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
