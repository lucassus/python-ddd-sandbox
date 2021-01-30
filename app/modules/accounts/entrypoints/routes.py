from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse

from app.modules.accounts.domain.service import Service
from app.modules.accounts.entrypoints import schemas
from app.modules.accounts.entrypoints.dependencies import get_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
def user_register_endpoint(
    data: schemas.RegisterUser,
    service: Service = Depends(get_service),
):
    user_id = service.register_user(email=data.email, password=data.password)

    return RedirectResponse(
        f"/users/{user_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
