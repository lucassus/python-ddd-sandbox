from typing import List

from databases import Database
from fastapi import APIRouter, Depends
from sqlalchemy import select

from todos.infrastructure.tables import projects_table
from todos.query_service import schemas
from todos.query_service.dependencies import get_database
from todos.query_service.errors import EntityNotFoundError

router = APIRouter()


@router.get(
    "",
    response_model=List[schemas.Project],
    name="Returns the list of projects",
)
async def projects_endpoint(database: Database = Depends(get_database)):
    query = select([projects_table])
    return await database.fetch_all(query=query)


@router.get("/{id}", response_model=schemas.Project)
async def project_endpoint(id: int, database: Database = Depends(get_database)):
    query = select([projects_table]).where(projects_table.c.id == id)
    row = await database.fetch_one(query=query)

    if row is None:
        raise EntityNotFoundError(detail=f"Unable to find a project with ID={id}")

    return row
