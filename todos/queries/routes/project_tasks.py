from typing import List

from fastapi import APIRouter, Path
from sqlalchemy import and_, select

from todos.adapters.sqlalchemy.tables import tasks_table
from todos.queries import schemas
from todos.queries.databases import database

router = APIRouter()


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks_table")
async def tasks_endpoint(project_id: int):
    query = select([tasks_table]).where(tasks_table.c.project_id == project_id)
    return await database.fetch_all(query=query)


# TODO: Figure out how to create an abstraction layer for raw sqls
@router.get("/{id}", response_model=schemas.Task)
async def task_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task", ge=1),
):
    query = select([tasks_table]).where(
        and_(
            tasks_table.c.project_id == project_id,
            tasks_table.c.id == id,
        )
    )
    return await database.fetch_one(query=query)

    # TODO: Create a cheat sheet
    # query = "SELECT * FROM tasks WHERE project_id = :project_id AND id = :id"
    # return await database.fetch_one(query=query, values={"project_id": project_id, "id": id})
