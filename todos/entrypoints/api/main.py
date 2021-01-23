from fastapi import FastAPI

from todos.adapters.databases import database
from todos.adapters.sqlalchemy.session import engine
from todos.adapters.sqlalchemy.tables import create_tables, start_mappers
from todos.entrypoints.api.routes import api_router

create_tables(engine)
start_mappers()


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


app = create_app()
