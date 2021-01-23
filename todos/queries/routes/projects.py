from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from todos.infrastructure.database import database
from todos.infrastructure.tables import projects_table
from todos.queries import schemas

router = APIRouter()


@router.get(
    "",
    response_model=List[schemas.Project],
    name="Returns the list of projects",
)
async def projects_endpoint():
    query = select([projects_table])
    return await database.fetch_all(query=query)


@router.get("/{id}", response_model=schemas.Project)
async def project_endpoint(id: int):
    query = select([projects_table]).where(projects_table.c.id == id)
    row = await database.fetch_one(query=query)

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a project with ID={id}",
        )

    return row
