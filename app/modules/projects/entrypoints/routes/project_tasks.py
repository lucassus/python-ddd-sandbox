from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

from app.modules.projects.application.queries.task_queries import GetTaskQuery
from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.entrypoints import schemas
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.entrypoints.errors import EntityNotFoundError
from app.modules.projects.entrypoints.routes.dependencies import get_project
from app.modules.projects.infrastructure.queries.task_queries import ListTasksSQLQuery

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
def task_endpoint(
    get_task: GetTaskQuery = Depends(Provide[Container.get_task_query]),
    project=Depends(get_project),
    number: int = Path(..., description="The number of the task", ge=1),
):
    task = get_task(project_id=project.id, number=TaskNumber(number))

    # TODO: Move it to the query
    if task is None:
        raise EntityNotFoundError(detail=f"Unable to find a task with {number=}")

    return task


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
