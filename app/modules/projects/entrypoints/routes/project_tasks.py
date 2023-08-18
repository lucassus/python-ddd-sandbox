from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Path, status
from starlette.responses import RedirectResponse

from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.application.queries.task_queries import GetTaskQuery
from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.entrypoints import schemas
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.entrypoints.dependencies import get_current_user
from app.modules.projects.infrastructure.queries.task_queries import ListTasksSQLQuery

router = APIRouter(prefix="/projects/{project_id}/tasks")


@router.post("")
@inject
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    current_user: Annotated[AuthenticationContract.CurrentUserDTO, Depends(get_current_user)],
    service: TasksService = Depends(Provide[Container.tasks_service]),
):
    task_number = service.create_task(
        project_id=ProjectID(project_id),
        created_by=current_user.id,
        name=data.name,
    )

    return RedirectResponse(
        f"/api/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "",
    name="Returns list of tasks",
    response_model=ListTasksSQLQuery.Result,
)
@inject
def list_tasks_endpoint(
    project_id: ProjectID,
    list_tasks: ListTasksSQLQuery = Depends(Provide[Container.list_tasks_query]),
):
    return list_tasks(project_id)


@router.get(
    "/{number}",
    response_model=GetTaskQuery.Result,
)
@inject
def get_task_endpoint(
    get_task: GetTaskQuery = Depends(Provide[Container.get_task_query]),
    project_id: ProjectID = Path(..., description="The ID of the project"),
    number: TaskNumber = Path(..., description="The number of the task", ge=1),
):
    try:
        return get_task(project_id, number)
    except GetTaskQuery.NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put("/{task_number}/complete")
@inject
def task_complete_endpoint(
    project_id: int,
    service: TasksService = Depends(Provide[Container.tasks_service]),
    task_number: int = Path(..., description="The number of the task to complete", ge=1),
):
    service.complete_task(ProjectID(project_id), TaskNumber(task_number))

    return RedirectResponse(
        f"/api/projects/{project_id}/tasks/{task_number}",
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
        f"/api/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
