from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.modules.accounts.application.containers import AppContainer
from app.modules.authentication_contract import AuthenticationContract

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/users/login",
    auto_error=True,
)


@inject
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    authentication: AuthenticationContract = Depends(Provide[AppContainer.authentication]),
) -> AuthenticationContract.Identity:
    return authentication.trade_token_for_user(token)
