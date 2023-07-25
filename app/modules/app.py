from importlib import import_module

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import registry

from app.shared.errors import EntityNotFoundError

APP_MODULES = ("accounts", "projects")


def create_app() -> FastAPI:
    app = FastAPI()

    # TODO: Where to put it?
    mapper_registry = registry()

    for name in APP_MODULES:
        module = import_module(f"app.modules.{name}")

        module.start_mappers(mapper_registry)
        app.include_router(module.router)

    @app.exception_handler(EntityNotFoundError)
    async def unicorn_exception_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )

    return app
