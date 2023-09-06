from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.commands import ChangeUserEmailAddress, RegisterUser
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.entrypoints import schemas
from app.modules.accounts.entrypoints.containers import Container
from app.modules.accounts.entrypoints.dependencies import get_current_user
from app.modules.accounts.queries.find_user_query import GetUserQuery
from app.modules.authentication_contract import AuthenticationContract
from app.modules.shared_kernel.message_bus import MessageBus

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
@inject
def user_register_endpoint(
    data: schemas.RegisterUser,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    try:
        bus.execute(RegisterUser(email=data.email, password=data.password))
    except EmailAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@router.post("/login")
@inject
def user_login_endpoint(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authentication: Authentication = Depends(Provide[Container.application.authentication]),
):
    data = schemas.LoginUser(email=form_data.username, password=form_data.password)
    token = authentication.login(email=data.email, password=data.password)

    return {
        "token_type": "bearer",
        "access_token": token,
    }


@router.put("/me")
@inject
def user_update_endpoint(
    current_user: Annotated[AuthenticationContract.CurrentUserDTO, Depends(get_current_user)],
    data: schemas.UpdateUser,
    bus: MessageBus = Depends(Provide[Container.bus]),
):
    bus.execute(
        ChangeUserEmailAddress(
            user_id=current_user.id,
            new_email=data.email,
        )
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
    return get_user(current_user.id)
