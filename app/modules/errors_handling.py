from fastapi import FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse

from app.modules.authentication_contract import AuthenticationError
from app.modules.shared_kernel.errors import EntityNotFoundError


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(EntityNotFoundError)
    def handle_entity_not_found_error(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AuthenticationError)
    def handler_authentication_error(request: Request, exc: AuthenticationError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )
