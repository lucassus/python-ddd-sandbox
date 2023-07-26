from typing import Annotated

from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.use_cases import RegisterUser
from app.modules.accounts.entrypoints import schemas
from app.modules.accounts.entrypoints.dependencies import get_register_user_use_case

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
def user_register_endpoint(
    data: schemas.RegisterUser,
    register_user: Annotated[RegisterUser, Depends(get_register_user_use_case)],
):
    # TODO: Handle EmailAlreadyExistsException and other errors, like invalid password
    user_id = register_user(
        email=EmailAddress(data.email),
        password=Password(data.password),
    )

    return RedirectResponse(
        f"/users/{user_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
