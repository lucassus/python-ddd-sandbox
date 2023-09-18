from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.commands import ChangeUserEmailAddress, RegisterUser
from app.modules.accounts.application.queries import GetUser
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.entrypoints import schemas
from app.modules.accounts.entrypoints.dependencies import get_current_user
from app.modules.accounts.application.containers import AppContainer
from app.modules.accounts.infrastructure.containers import QueriesContainer
from app.modules.accounts.infrastructure.queries import GetUserQueryHandler
from app.modules.authentication_contract import AuthenticationContract
from app.shared.message_bus import MessageBus

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
@inject
def user_register_endpoint(
    data: schemas.RegisterUser,
    bus: MessageBus = Depends(Provide[AppContainer.bus]),
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
    authentication: Authentication = Depends(Provide[AppContainer.authentication]),
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
    current_user: Annotated[AuthenticationContract.Identity, Depends(get_current_user)],
    data: schemas.UpdateUser,
    bus: MessageBus = Depends(Provide[AppContainer.bus]),
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
    response_model=GetUser.Result,
)
@inject
async def user_endpoint(
    current_user: Annotated[AuthenticationContract.Identity, Depends(get_current_user)],
    handle: GetUserQueryHandler = Depends(Provide[QueriesContainer.get_user]),
):
    return await handle(GetUser(current_user.id))
