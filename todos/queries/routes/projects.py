from typing import List

from fastapi import APIRouter
from sqlalchemy import select

from todos.infrastructure.database import database
from todos.infrastructure.tables import projects_table
from todos.queries import schemas

router = APIRouter()


# TODO: Write test


@router.get(
    "",
    response_model=List[schemas.Project],
    name="Returns list of projects",
)
async def projects_endpoint():
    query = select([projects_table])
    return await database.fetch_all(query=query)


@router.get("/{id}", response_model=schemas.Project)
async def project_endpoint(id: int):
    query = select([projects_table]).where(projects_table.c.id == id)
    return await database.fetch_one(query=query)
