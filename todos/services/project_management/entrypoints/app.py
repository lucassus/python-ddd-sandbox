from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from todos.common.errors import EntityNotFoundError
from todos.infrastructure.session import engine
from todos.infrastructure.tables import create_tables
from todos.services.project_management.adapters.mappers import start_mappers
from todos.services.project_management.entrypoints.routes import api_router

create_tables(engine)
start_mappers()


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    # TODO: Add similar error handler for MaxIncompleteTasksNumberIsReached
    @app.exception_handler(EntityNotFoundError)
    async def unicorn_exception_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )

    return app
