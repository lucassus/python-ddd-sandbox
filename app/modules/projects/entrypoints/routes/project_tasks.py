from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

import app.modules.projects.application.queries.task_queries
from app.modules.projects.application.queries.project_queries import FindProjectQueryProtocol
from app.modules.projects.application.queries.task_queries import FindTaskQueryProtocol
from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.entrypoints import schemas
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.entrypoints.errors import EntityNotFoundError
from app.modules.projects.infrastructure.queries.task_queries import ListTasksQuery

router = APIRouter(prefix="/projects/{project_id}/tasks")


# TODO: Drop it
@inject
def get_project(
    project_id: int,
    find_project: FindProjectQueryProtocol = Depends(Provide[Container.find_project_query]),
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
        f"/api/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "",
    response_model=list[app.modules.projects.application.queries.task_queries.Task],
    name="Returns list of tasks",
)
@inject
def tasks_endpoint(
    list_tasks: ListTasksQuery = Depends(Provide[Container.list_tasks_query]),
    project=Depends(get_project),
):
    tasks = list_tasks(project_id=project.id)
    return [app.modules.projects.application.queries.task_queries.Task.from_orm(task) for task in tasks]


@router.get(
    "/{number}",
    response_model=app.modules.projects.application.queries.task_queries.Task,
)
@inject
def task_endpoint(
    find_task: FindTaskQueryProtocol = Depends(Provide[Container.find_task_query]),
    project=Depends(get_project),
    number: int = Path(..., description="The number of the task", ge=1),
):
    task = find_task(project_id=project.id, number=TaskNumber(number))

    if task is None:
        raise EntityNotFoundError(detail=f"Unable to find a task with {number=}")

    # TODO: Remove this deprecated code
    return app.modules.projects.application.queries.task_queries.Task.from_orm(task)


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
