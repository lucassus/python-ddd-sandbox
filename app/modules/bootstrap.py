from importlib import import_module

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.common.errors import EntityNotFoundError

# TODO: Refactor it
BOUNDED_CONTEXTS = ("accounts", "projects")


def start_all_mappers():
    for context in BOUNDED_CONTEXTS:
        module = import_module(f"app.modules.{context}.adapters.mappers")
        module.start_mappers()


start_all_mappers()


def create_app() -> FastAPI:
    app = FastAPI()

    def include_all_routes():
        for context in BOUNDED_CONTEXTS:
            module = import_module(f"app.modules.{context}.entrypoints.routes")
            app.include_router(module.api_router)

    include_all_routes()

    @app.exception_handler(EntityNotFoundError)
    async def unicorn_exception_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )

    return app
