from fastapi import APIRouter, Depends

from app.query import schemas
from app.query.errors import EntityNotFoundError
from app.query.queries.projects import FetchProjectsQuery
from app.query.queries.users import FindUserQuery

router = APIRouter()


@router.get(
    "/{id}",
    response_model=schemas.User,
    name="Returns the list of projects",
)
async def user_endpoint(
    id: int,
    find_user: FindUserQuery = Depends(),
    fetch_projects: FetchProjectsQuery = Depends(),
):
    user = await find_user(id=id)

    if user is None:
        raise EntityNotFoundError(detail=f"Unable to find a user with ID={id}")

    projects = await fetch_projects(user_id=id)

    return dict(user, projects=[dict(project) for project in projects])
