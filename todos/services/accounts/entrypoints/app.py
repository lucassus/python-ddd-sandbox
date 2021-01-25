from fastapi import FastAPI

from todos.infrastructure.session import engine
from todos.infrastructure.tables import create_tables
from todos.services.accounts.adapters.mappers import start_mappers
from todos.services.accounts.entrypoints.routes import api_router

# TODO: Move it to the other place
create_tables(engine)
start_mappers()


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    return app
