from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import RedirectResponse

from app.modules.accounts.application.change_user_email_address import ChangeUserEmailAddress
from app.modules.accounts.application.queries.find_user_query import GetUserQuery
from app.modules.accounts.application.register_user import RegisterUser
from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.entrypoints import schemas
from app.modules.accounts.entrypoints.containers import Container
from app.modules.shared_kernel.entities.user_id import UserID

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
@inject
def user_register_endpoint(
    data: schemas.RegisterUser,
    register_user: RegisterUser = Depends(Provide[Container.register_user]),
):
    try:
        user_id = register_user(
            email=EmailAddress(data.email),
            password=Password(data.password),
        )
    except EmailAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e

    return RedirectResponse(
        f"/api/users/{user_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{user_id}")
@inject
def user_update_endpoint(
    user_id: int,
    data: schemas.UpdateUser,
    change_user_email_address: ChangeUserEmailAddress = Depends(Provide[Container.change_user_email_address]),
):
    change_user_email_address(
        user_id=UserID(user_id),
        new_email=EmailAddress(data.email),
    )

    return RedirectResponse(
        f"/api/users/{user_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "/{user_id}",
    name="Returns user along with projects",
    response_model=GetUserQuery.Result,
)
@inject
def user_endpoint(
    user_id: int,
    get_user: GetUserQuery = Depends(Provide[Container.get_user_query]),
):
    try:
        return get_user(id=UserID(user_id))
    except GetUserQuery.NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
