from databases import Database
from fastapi import APIRouter, Depends
from sqlalchemy import select

from todos.infrastructure.tables import projects_table, users_table
from todos.query_service import schemas
from todos.query_service.dependencies import get_database
from todos.query_service.errors import EntityNotFoundError

router = APIRouter()


@router.get(
    "/{id}",
    response_model=schemas.User,
    name="Returns the list of projects",
)
async def user_endpoint(id: int, database: Database = Depends(get_database)):
    query = select([users_table]).where(users_table.c.id == id)
    user = await database.fetch_one(query=query)

    if user is None:
        raise EntityNotFoundError(detail=f"Unable to find a user with ID={id}")

    query = select([projects_table]).where(projects_table.c.user_id == id)
    projects = await database.fetch_all(query=query)

    return dict(user, projects=[dict(project) for project in projects])
