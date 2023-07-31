from typing import Annotated

from fastapi import APIRouter, Depends, Path

from app.query import schemas
from app.query.dependencies import get_project
from app.query.errors import EntityNotFoundError
from app.query.queries.tasks import FetchTasksQuery, FindTaskQuery

router = APIRouter()


@router.get("", response_model=list[schemas.Task], name="Returns list of tasks")
def tasks_endpoint(
    list_tasks: Annotated[FetchTasksQuery, Depends()],
    project=Depends(get_project),
):
    tasks = list_tasks(project_id=project.id)
    return [schemas.Task.from_orm(task) for task in tasks]


@router.get("/{number}", response_model=schemas.Task)
def task_endpoint(
    find_task: Annotated[FindTaskQuery, Depends()],
    project=Depends(get_project),
    number: int = Path(..., description="The number of the task", ge=1),
):
    task = find_task(project_id=project.id, number=number)

    if task is None:
        raise EntityNotFoundError(detail=f"Unable to find a task with {number=}")

    return schemas.Task.from_orm(task)
