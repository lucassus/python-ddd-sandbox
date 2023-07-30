from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import registry

from app.modules.accounts import register_module as register_accounts_module
from app.modules.projects import register_module as register_projects_module
from app.shared_kernel.errors import EntityNotFoundError

mapper_registry = registry()


def create_app() -> FastAPI:
    app = FastAPI()

    register_accounts_module(app, mapper_registry)
    register_projects_module(app, mapper_registry)

    @app.exception_handler(EntityNotFoundError)
    async def unicorn_exception_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    return app
