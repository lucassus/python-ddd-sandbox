from typing import Protocol

from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import registry

from app.modules import accounts, projects
from app.shared.errors import EntityNotFoundError


class AppModule(Protocol):
    router: APIRouter

    def start_mappers(self, mapper_registry: registry) -> None:
        ...


mapper_registry = registry()


def _register_module(app: FastAPI, module: AppModule) -> None:
    module.start_mappers(mapper_registry)
    app.include_router(module.router)


def create_app() -> FastAPI:
    app = FastAPI()

    _register_module(app, accounts)
    _register_module(app, projects)

    @app.exception_handler(EntityNotFoundError)
    async def unicorn_exception_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )

    return app
