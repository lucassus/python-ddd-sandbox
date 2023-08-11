from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

from app.command.projects.application.tasks_service import TasksService
from app.command.projects.domain.project import ProjectID
from app.command.projects.domain.task import TaskNumber
from app.command.projects.entrypoints import schemas
from app.command.projects.entrypoints.containers import Container

router = APIRouter(prefix="/projects/{project_id}/tasks")


@router.post("")
@inject
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    service: TasksService = Depends(Provide[Container.tasks_service]),
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
@inject
def task_complete_endpoint(
    project_id: int,
    service: TasksService = Depends(Provide[Container.tasks_service]),
    task_number: int = Path(..., description="The number of the task to complete", ge=1),
):
    service.complete_task(ProjectID(project_id), TaskNumber(task_number))

    return RedirectResponse(
        f"/queries/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{task_number}/incomplete")
@inject
def task_incomplete_endpoint(
    project_id: int,
    service: TasksService = Depends(Provide[Container.tasks_service]),
    task_number: int = Path(..., description="The number of the task to incomplete", ge=1),
):
    service.incomplete_task(ProjectID(project_id), TaskNumber(task_number))

    return RedirectResponse(
        f"/queries/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
