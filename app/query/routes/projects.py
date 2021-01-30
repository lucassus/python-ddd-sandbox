from typing import List

from databases import Database
from fastapi import APIRouter, Depends

from app.infrastructure.tables import projects_table
from app.query import schemas
from app.query.dependencies import get_database, get_project

router = APIRouter()


@router.get(
    "",
    response_model=List[schemas.Project],
    name="Returns the list of projects",
)
async def projects_endpoint(database: Database = Depends(get_database)):
    query = projects_table.select()
    return await database.fetch_all(query=query)


@router.get("/{project_id}", response_model=schemas.Project)
async def project_endpoint(project=Depends(get_project)):
    return project
