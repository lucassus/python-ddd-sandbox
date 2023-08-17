from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Header, HTTPException
from starlette import status

from app.modules.accounts.application.authentication import Authentication, AuthenticationError
from app.modules.accounts.entrypoints.containers import Container

# TODO: Implement a more robust authentication, see https://fastapi.tiangolo.com/tutorial/security/


@inject
def get_current_user(
    authentication: Authentication = Depends(Provide[Container.authenticate]),
    x_authentication_token: Annotated[str | None, Header()] = None,
) -> Authentication.UserDTO:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    if x_authentication_token is None:
        raise credentials_exception

    try:
        return authentication.trade_token_for_user(x_authentication_token)
    except AuthenticationError:
        raise credentials_exception
