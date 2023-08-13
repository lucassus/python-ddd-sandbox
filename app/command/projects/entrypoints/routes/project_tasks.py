from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

from app.command.projects.application.queries.project_queries import AbstractFindProjectQuery
from app.command.projects.application.queries.task_queries import AbstractFindTaskQuery
from app.command.projects.application.tasks_service import TasksService
from app.command.projects.domain.project import ProjectID
from app.command.projects.domain.task import TaskNumber
from app.command.projects.entrypoints import schemas
from app.command.projects.entrypoints.containers import Container
from app.command.projects.entrypoints.errors import EntityNotFoundError
from app.command.projects.infrastructure.queries.task_queries import FetchTasksQuery

router = APIRouter(prefix="/projects/{project_id}/tasks")


# TODO: Drop it
@inject
def get_project(
    project_id: int,
    find_project: AbstractFindProjectQuery = Depends(Provide[Container.find_project_query]),
):
    return find_project(id=ProjectID(project_id))


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
        f"/commands/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "",
    response_model=list[schemas.Task],
    name="Returns list of tasks",
)
@inject
def tasks_endpoint(
    list_tasks: FetchTasksQuery = Depends(Provide[Container.list_tasks_query]),
    project=Depends(get_project),
):
    tasks = list_tasks(project_id=project.id)
    return [schemas.Task.from_orm(task) for task in tasks]


@router.get(
    "/{number}",
    response_model=schemas.Task,
)
@inject
def task_endpoint(
    find_task: AbstractFindTaskQuery = Depends(Provide[Container.find_task_query]),
    project=Depends(get_project),
    number: int = Path(..., description="The number of the task", ge=1),
):
    task = find_task(project_id=project.id, number=TaskNumber(number))

    if task is None:
        raise EntityNotFoundError(detail=f"Unable to find a task with {number=}")

    # TODO: Remove this deprecated code
    return schemas.Task.from_orm(task)


@router.put("/{task_number}/complete")
@inject
def task_complete_endpoint(
    project_id: int,
    service: TasksService = Depends(Provide[Container.tasks_service]),
    task_number: int = Path(..., description="The number of the task to complete", ge=1),
):
    service.complete_task(ProjectID(project_id), TaskNumber(task_number))

    return RedirectResponse(
        f"/commands/projects/{project_id}/tasks/{task_number}",
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
        f"/commands/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
