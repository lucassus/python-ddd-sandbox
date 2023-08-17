from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Header

from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.entrypoints.containers import Container


@inject
def get_current_user(
    authentication: Authentication = Depends(Provide[Container.authenticate]),
    x_authentication_token: Annotated[str | None, Header()] = None,  # TODO: Improve this
) -> Authentication.UserDTO | None:
    if x_authentication_token is None:
        return None

    return authentication.trade_token_for_user(x_authentication_token)
