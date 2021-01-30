from databases import Database
from fastapi import APIRouter, Depends

from app.infrastructure.tables import projects_table, users_table
from app.query import schemas
from app.query.dependencies import get_database
from app.query.errors import EntityNotFoundError

router = APIRouter()


@router.get(
    "/{id}",
    response_model=schemas.User,
    name="Returns the list of projects",
)
async def user_endpoint(id: int, database: Database = Depends(get_database)):
    query = users_table.select().where(users_table.c.id == id)
    user = await database.fetch_one(query=query)

    if user is None:
        raise EntityNotFoundError(detail=f"Unable to find a user with ID={id}")

    query = projects_table.select().where(projects_table.c.user_id == id)
    projects = await database.fetch_all(query=query)

    return dict(user, projects=[dict(project) for project in projects])
