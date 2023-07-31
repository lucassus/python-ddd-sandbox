from typing import Annotated

from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse

from app.command.accounts.application.change_user_email_address import ChangeUserEmailAddress
from app.command.accounts.application.register_user import RegisterUser
from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password
from app.command.accounts.entrypoints import schemas
from app.command.accounts.entrypoints.dependencies import get_change_user_email_address, get_register_user
from app.shared_kernel.user_id import UserID

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
def user_register_endpoint(
    data: schemas.RegisterUser,
    register_user: Annotated[RegisterUser, Depends(get_register_user)],
):
    # TODO: Handle EmailAlreadyExistsException and other errors, like invalid password
    user_id = register_user(
        email=EmailAddress(data.email),
        password=Password(data.password),
    )

    return RedirectResponse(
        f"/queries/users/{user_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{user_id}")
def user_update_endpoint(
    user_id: int,
    data: schemas.UpdateUser,
    change_user_email_address: Annotated[ChangeUserEmailAddress, Depends(get_change_user_email_address)],
):
    change_user_email_address(
        user_id=UserID(user_id),
        new_email=EmailAddress(data.email),
    )

    return RedirectResponse(
        f"/queries/users/{user_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
