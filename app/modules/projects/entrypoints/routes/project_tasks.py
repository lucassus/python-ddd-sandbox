from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.application.commands.complete_task import CompleteTask
from app.modules.projects.application.commands.create_task import CreateTask
from app.modules.projects.application.commands.incomplete_task import IncompleteTask
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.entrypoints import schemas
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.entrypoints.dependencies import get_current_user
from app.modules.projects.queries.task_queries import GetTaskQuery, ListTasksQuery
from app.modules.shared_kernel.message_bus import MessageBus
from app.utc_datetime import utc_now

router = APIRouter(prefix="/projects/{project_id}/tasks")


@router.post("")
@inject
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    current_user: Annotated[AuthenticationContract.CurrentUserDTO, Depends(get_current_user)],
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    task_number = bus.execute(
        CreateTask(
            project_id=ProjectID(project_id),
            created_by=current_user.id,
            name=data.name,
        ),
    )

    return RedirectResponse(
        f"/api/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "",
    name="Returns list of tasks",
    response_model=ListTasksQuery.Result,
)
@inject
def list_tasks_endpoint(
    project_id: ProjectID,
    list_tasks: ListTasksQuery = Depends(Provide[Container.queries.list_tasks]),
):
    return list_tasks(project_id)


@router.get(
    "/{number}",
    response_model=GetTaskQuery.Result,
)
@inject
def get_task_endpoint(
    get_task: GetTaskQuery = Depends(Provide[Container.queries.get_task]),
    project_id: ProjectID = Path(..., description="The ID of the project"),
    number: TaskNumber = Path(..., description="The number of the task", ge=1),
):
    return get_task(project_id, number)


@router.put("/{task_number}/complete")
@inject
def task_complete_endpoint(
    project_id: int,
    task_number: int = Path(..., description="The number of the task to complete", ge=1),
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    bus.execute(
        CompleteTask(
            project_id=ProjectID(project_id),
            task_number=TaskNumber(task_number),
            now=utc_now(),
        ),
    )

    return RedirectResponse(
        f"/api/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{task_number}/incomplete")
@inject
def task_incomplete_endpoint(
    project_id: int,
    task_number: int = Path(..., description="The number of the task to incomplete", ge=1),
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    bus.execute(
        IncompleteTask(
            project_id=ProjectID(project_id),
            task_number=TaskNumber(task_number),
        )
    )

    return RedirectResponse(
        f"/api/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
