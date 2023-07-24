from fastapi import APIRouter, Depends, Path

from app.query import schemas
from app.query.dependencies import get_project
from app.query.errors import EntityNotFoundError
from app.query.queries.tasks import FetchTasksQuery, FindTaskQuery

router = APIRouter()


@router.get("", response_model=list[schemas.Task], name="Returns list of tasks")
def tasks_endpoint(
    project=Depends(get_project),
    list_tasks: FetchTasksQuery = Depends(),
):
    tasks = list_tasks(project_id=project.id)
    return [schemas.Task.from_orm(task) for task in tasks]


@router.get("/{id}", response_model=schemas.Task)
def task_endpoint(
    project=Depends(get_project),
    id: int = Path(..., description="The ID of the task", ge=1),
    find_task: FindTaskQuery = Depends(),
):
    task = find_task(project_id=project.id, task_id=id)

    if task is None:
        raise EntityNotFoundError(detail=f"Unable to find a task with ID={id}")

    return schemas.Task.from_orm(task)
