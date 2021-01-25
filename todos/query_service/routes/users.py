from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from todos.infrastructure.tables import users_table
from todos.query_service import schemas
from todos.query_service.dependencies import get_database

router = APIRouter()


@router.get(
    "/{id}",
    response_model=schemas.User,
    name="Returns the list of projects",
)
async def user_endpoint(id: int, database=Depends(get_database)):
    query = select([users_table]).where(users_table.c.id == id)
    user = await database.fetch_one(query=query)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find a user with ID={id}",
        )

    return user
