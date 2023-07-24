from typing import List

from fastapi import APIRouter, Depends, Path

from app.query import schemas
from app.query.dependencies import get_project
from app.query.errors import EntityNotFoundError
from app.query.queries.tasks import FetchTasksQuery, FindTaskQuery

router = APIRouter()

# TODO: Unit test for the API
# TODO: Integration tests for the queries


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks")
def tasks_endpoint(
    project=Depends(get_project),
    list_tasks: FetchTasksQuery = Depends(),
):
    return list_tasks(project_id=project.id)


@router.get("/{id}", response_model=schemas.Task)
def task_endpoint(
    project=Depends(get_project),
    id: int = Path(..., description="The ID of the task", ge=1),
    find_task: FindTaskQuery = Depends(),
):
    task = find_task(project_id=project.id, task_id=id)

    if task is None:
        raise EntityNotFoundError(detail=f"Unable to find a task with ID={id}")

    return task
