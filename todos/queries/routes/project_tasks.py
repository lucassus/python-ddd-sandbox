from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import and_, select

from todos.infrastructure.tables import tasks_table
from todos.queries import schemas
from todos.queries.dependencies import get_database

router = APIRouter()


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks_table")
async def tasks_endpoint(project_id: int, database=Depends(get_database)):
    query = select([tasks_table]).where(tasks_table.c.project_id == project_id)
    return await database.fetch_all(query=query)


@router.get("/{id}", response_model=schemas.Task)
async def task_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task", ge=1),
    database=Depends(get_database),
):
    query = select([tasks_table]).where(
        and_(
            tasks_table.c.project_id == project_id,
            tasks_table.c.id == id,
        )
    )
    row = await database.fetch_one(query=query)

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a task with ID={id}",
        )

    return row
