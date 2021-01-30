from typing import List

from databases import Database
from fastapi import APIRouter, Depends, Path
from sqlalchemy import and_

from app.infrastructure.tables import tasks_table
from app.query_service import schemas
from app.query_service.dependencies import get_database
from app.query_service.errors import EntityNotFoundError

router = APIRouter()


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks_table")
async def tasks_endpoint(
    project_id: int,
    database: Database = Depends(get_database),
):
    query = tasks_table.select().where(tasks_table.c.project_id == project_id)
    return await database.fetch_all(query=query)


@router.get("/{id}", response_model=schemas.Task)
async def task_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task", ge=1),
    database: Database = Depends(get_database),
):
    query = tasks_table.select().where(
        and_(
            tasks_table.c.project_id == project_id,
            tasks_table.c.id == id,
        )
    )
    row = await database.fetch_one(query=query)

    if row is None:
        raise EntityNotFoundError(detail=f"Unable to find a task with ID={id}")

    return row
