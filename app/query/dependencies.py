from databases import Database
from fastapi import Depends, Request

from app.infrastructure.tables import projects_table
from app.query.errors import EntityNotFoundError


def get_database(request: Request) -> Database:
    return request.state.database


async def get_project(project_id: int, database: Database = Depends(get_database)):
    query = projects_table.select().where(projects_table.c.id == project_id)
    row = await database.fetch_one(query=query)

    if row is None:
        raise EntityNotFoundError(
            detail=f"Unable to find a project with ID={project_id}"
        )

    return row
