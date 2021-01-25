from importlib import import_module

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from todos.common.errors import EntityNotFoundError
from todos.services.accounts.entrypoints.routes import api_router as api_router_2
from todos.services.project_management.entrypoints.routes import (
    api_router as api_router_1,
)


def start_all_mappers():
    for context in ("accounts", "project_management"):
        mappers = import_module(f"todos.services.{context}.adapters.mappers")
        mappers.start_mappers()


start_all_mappers()


def create_app() -> FastAPI:
    app = FastAPI()

    # TODO: Figure out how to refactor it
    app.include_router(api_router_1)
    app.include_router(api_router_2)

    @app.exception_handler(EntityNotFoundError)
    async def unicorn_exception_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )

    return app
