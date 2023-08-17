from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.modules.accounts.application.authentication import Authentication, AuthenticationError
from app.modules.accounts.entrypoints.containers import Container

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


@inject
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    authentication: Authentication = Depends(Provide[Container.authenticate]),
) -> Authentication.UserDTO:
    try:
        return authentication.trade_token_for_user(token)
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
