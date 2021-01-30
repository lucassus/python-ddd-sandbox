from typing import List

from databases import Database
from fastapi import APIRouter, Depends

from app.infrastructure.tables import projects_table
from app.query_service import schemas
from app.query_service.dependencies import get_database
from app.query_service.errors import EntityNotFoundError

router = APIRouter()


@router.get(
    "",
    response_model=List[schemas.Project],
    name="Returns the list of projects",
)
async def projects_endpoint(database: Database = Depends(get_database)):
    query = projects_table.select()
    return await database.fetch_all(query=query)


@router.get("/{id}", response_model=schemas.Project)
async def project_endpoint(id: int, database: Database = Depends(get_database)):
    query = projects_table.select().where(projects_table.c.id == id)
    row = await database.fetch_one(query=query)

    if row is None:
        raise EntityNotFoundError(detail=f"Unable to find a project with ID={id}")

    return row
