from importlib import import_module

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.common.errors import EntityNotFoundError


def create_app() -> FastAPI:
    app = FastAPI()

    for name in ("accounts", "projects"):
        module = import_module(f"app.modules.{name}")

        module.start_mappers()
        app.include_router(module.router)

    @app.exception_handler(EntityNotFoundError)
    async def unicorn_exception_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )

    return app
