from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from todos.common.errors import EntityNotFoundError
from todos.services.accounts.entrypoints.routes import api_router as api_router_2
from todos.services.project_management.entrypoints.routes import (
    api_router as api_router_1,
)


# TODO: Figure out how to refactor it
def start_mappers():
    from todos.services.accounts.adapters.mappers import (
        start_mappers as start_accounts_mappers,
    )
    from todos.services.project_management.adapters.mappers import (
        start_mappers as start_project_management_mappers,
    )

    start_accounts_mappers()
    start_project_management_mappers()


start_mappers()


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
