from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

from app.modules.projects.application.commands import CompleteTask, CreateTask, IncompleteTask
from app.modules.projects.application.queries import GetTask, ListTasks
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.entrypoints import schemas
from app.modules.projects.infrastructure.containers import Container
from app.modules.projects.infrastructure.queries.task_query_handlers import GetTaskQueryHandler, ListTasksQueryHandler
from app.shared.message_bus import MessageBus
from app.utc_datetime import utc_now

router = APIRouter(prefix="/projects/{project_id}/tasks")


@router.post("")
@inject
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    task_number = bus.execute(CreateTask(ProjectID(project_id), name=data.name))

    return RedirectResponse(
        f"/api/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "",
    name="Returns list of tasks",
    response_model=ListTasks.Result,
)
@inject
async def list_tasks_endpoint(
    project_id: ProjectID,
    handle: ListTasksQueryHandler = Depends(Provide[Container.queries.list_tasks_handler]),
):
    return await handle(ListTasks(project_id))


@router.get(
    "/{number}",
    response_model=GetTask.Result,
)
@inject
async def get_task_endpoint(
    handle: GetTaskQueryHandler = Depends(Provide[Container.queries.get_task_handler]),
    project_id: ProjectID = Path(..., description="The ID of the project"),
    number: TaskNumber = Path(..., description="The number of the task", ge=1),
):
    return await handle(GetTask(project_id, number))


@router.put("/{task_number}/complete")
@inject
def task_complete_endpoint(
    project_id: int,
    task_number: int = Path(..., description="The number of the task to complete", ge=1),
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    bus.execute(CompleteTask(ProjectID(project_id), TaskNumber(task_number), now=utc_now()))

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
    bus.execute(IncompleteTask(ProjectID(project_id), TaskNumber(task_number)))

    return RedirectResponse(
        f"/api/projects/{project_id}/tasks/{task_number}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
