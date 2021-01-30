from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.common.errors import EntityNotFoundError


def create_app() -> FastAPI:
    app = FastAPI()

    from app.modules.accounts import router, start_mappers

    start_mappers()
    app.include_router(router)

    from app.modules.projects import router, start_mappers

    start_mappers()
    app.include_router(router)

    @app.exception_handler(EntityNotFoundError)
    async def unicorn_exception_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )

    return app
