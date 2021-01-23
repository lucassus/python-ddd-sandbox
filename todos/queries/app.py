from fastapi import FastAPI

from todos.infrastructure.database import database
from todos.queries.routes import api_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    return app
