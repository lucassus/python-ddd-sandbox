from typing import Annotated

from fastapi import APIRouter, Depends

from app.query import schemas
from app.query.errors import EntityNotFoundError
from app.query.queries.users import FindUserQuery

router = APIRouter()


@router.get(
    "/{id}",
    response_model=schemas.User,
    name="Returns user along with projects",
)
def user_endpoint(
    id: int,
    find_user: Annotated[FindUserQuery, Depends()],
):
    user = find_user(id=id)

    if user is None:
        raise EntityNotFoundError(detail=f"Unable to find a user with ID={id}")

    return user
