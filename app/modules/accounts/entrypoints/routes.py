from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import RedirectResponse

from app.modules.accounts.application.authentication import Authentication, AuthenticationError
from app.modules.accounts.application.change_user_email_address import ChangeUserEmailAddress
from app.modules.accounts.application.jwt import JWT
from app.modules.accounts.application.queries.find_user_query import GetUserQuery
from app.modules.accounts.application.register_user import RegisterUser
from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.entrypoints import schemas
from app.modules.accounts.entrypoints.containers import Container
from app.modules.accounts.entrypoints.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
@inject
def user_register_endpoint(
    data: schemas.RegisterUser,
    register_user: RegisterUser = Depends(Provide[Container.register_user]),
    jwt: JWT = Depends(Provide[Container.jwt]),
):
    try:
        user_id = register_user(
            email=EmailAddress(data.email),
            password=Password(data.password),
        )
    except EmailAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    return {"token": jwt.encode(user_id)}


@router.post("/login")
@inject
def user_login_endpoint(
    data: schemas.LoginUser,
    authentication: Authentication = Depends(Provide[Container.authenticate]),
):
    try:
        token = authentication.login(
            email=EmailAddress(data.email),
            password=Password(data.password),
        )
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e

    return {"token": token}


@router.put("/me")
@inject
def user_update_endpoint(
    current_user: Annotated[Authentication.UserDTO, Depends(get_current_user)],
    data: schemas.UpdateUser,
    change_user_email_address: ChangeUserEmailAddress = Depends(Provide[Container.change_user_email_address]),
):
    change_user_email_address(
        user_id=current_user.id,
        new_email=EmailAddress(data.email),
    )

    return RedirectResponse(
        "/api/users/me",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "/me",
    name="Returns the current user along with projects",
    response_model=GetUserQuery.Result,
)
@inject
def user_endpoint(
    current_user: Annotated[Authentication.UserDTO, Depends(get_current_user)],
    get_user: GetUserQuery = Depends(Provide[Container.get_user_query]),
):
    try:
        return get_user(current_user.id)
    except GetUserQuery.NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
