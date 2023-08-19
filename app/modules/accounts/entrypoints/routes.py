from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.change_user_email_address import ChangeUserEmailAddress
from app.modules.accounts.application.jwt import JWT
from app.modules.accounts.application.register_user import RegisterUser
from app.modules.accounts.containers import Container
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.entrypoints import schemas
from app.modules.accounts.entrypoints.dependencies import get_current_user
from app.modules.accounts.queries.find_user_query import GetUserQuery
from app.modules.authentication_contract import AuthenticationContract, AuthenticationError
from app.modules.shared_kernel.entities.email_address import EmailAddress

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
@inject
def user_register_endpoint(
    data: schemas.RegisterUser,
    register_user: RegisterUser = Depends(Provide[Container.application.register_user]),
    jwt: JWT = Depends(Provide[Container.application.jwt]),
):
    try:
        user_id = register_user(
            email=EmailAddress(data.email),
            password=Password(data.password),
        )
    except EmailAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    return {
        "token_type": "bearer",
        "access_token": jwt.encode(user_id),
    }


@router.post("/login")
@inject
def user_login_endpoint(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authentication: Authentication = Depends(Provide[Container.application.authentication]),
):
    try:
        token = authentication.login(
            email=EmailAddress(form_data.username),
            password=Password(form_data.password),
        )
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e

    return {
        "token_type": "bearer",
        "access_token": token,
    }


@router.put("/me")
@inject
def user_update_endpoint(
    current_user: Annotated[AuthenticationContract.CurrentUserDTO, Depends(get_current_user)],
    data: schemas.UpdateUser,
    change_user_email_address: ChangeUserEmailAddress = Depends(
        Provide[Container.application.change_user_email_address]
    ),
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
    current_user: Annotated[AuthenticationContract.CurrentUserDTO, Depends(get_current_user)],
    get_user: GetUserQuery = Depends(Provide[Container.queries.get_user]),
):
    try:
        return get_user(current_user.id)
    except GetUserQuery.NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
