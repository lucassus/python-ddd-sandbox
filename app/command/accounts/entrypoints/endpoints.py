from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import RedirectResponse

from app.command.accounts.application.change_user_email_address import ChangeUserEmailAddress
from app.command.accounts.application.queries import schemas as query_schemas
from app.command.accounts.application.register_user import RegisterUser
from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.errors import EmailAlreadyExistsException
from app.command.accounts.entities.password import Password
from app.command.accounts.entrypoints import schemas as command_schemas
from app.command.accounts.entrypoints.containers import Container
from app.command.accounts.infrastructure.queries.find_user_query import FindUserQuery
from app.command.shared_kernel.entities.user_id import UserID

router = APIRouter(prefix="/users", tags=["users"])


# TODO: Is is a good idea to have separate query and command schemas?


@router.post("")
@inject
def user_register_endpoint(
    data: command_schemas.RegisterUser,
    register_user: RegisterUser = Depends(Provide[Container.register_user]),
):
    try:
        user_id = register_user(
            email=EmailAddress(data.email),
            password=Password(data.password),
        )
    except EmailAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    return RedirectResponse(
        f"/commands/users/{user_id}",  # TODO: Change this route
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "/{id}",
    response_model=query_schemas.UserDetails,
    name="Returns user along with projects",
)
@inject
def user_endpoint(
    id: int,
    # TODO: Use dependency injection container
    find_user: Annotated[FindUserQuery, Depends()],
):
    user = find_user(id=id)

    # TODO: Move it to the query class
    # if user is None:
    #     raise EntityNotFoundError(detail=f"Unable to find a user with ID={id}")

    return user


@router.put("/{user_id}")
@inject
def user_update_endpoint(
    user_id: int,
    data: command_schemas.UpdateUser,
    change_user_email_address: ChangeUserEmailAddress = Depends(Provide[Container.change_user_email_address]),
):
    change_user_email_address(
        user_id=UserID(user_id),
        new_email=EmailAddress(data.email),
    )

    return RedirectResponse(
        f"/commands/users/{user_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
