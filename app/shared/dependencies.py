from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.modules.authentication_contract import AuthenticationContract
from app.shared.message_bus import MessageBus


# TODO: Is it a good idea?
def get_message_bus():
    # Override this function during application creation
    raise NotImplementedError


MessageBusDep = Annotated[MessageBus, Depends(get_message_bus)]


def get_authentication():
    # Override this function during application creation
    raise NotImplementedError


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/users/login",
    auto_error=True,
)


def get_current_user(
    authentication: Annotated[AuthenticationContract, Depends(get_authentication)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> AuthenticationContract.CurrentUserDTO:
    return authentication.trade_token_for_user(token)


CurrentUserDep = Annotated[AuthenticationContract.CurrentUserDTO, Depends(get_current_user)]
