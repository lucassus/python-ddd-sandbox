from fastapi import FastAPI

from todos.commands.adapters.sqlalchemy.mappers import start_mappers
from todos.commands.entrypoints.api.routes import api_router
from todos.infrastructure.session import engine
from todos.infrastructure.tables import create_tables

create_tables(engine)
start_mappers()


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    return app
