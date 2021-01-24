from fastapi import FastAPI

from todos.infrastructure.session import engine
from todos.infrastructure.tables import create_tables
from todos.services.project_management.adapters.mappers import start_mappers
from todos.services.project_management.entrypoints.routes import api_router

create_tables(engine)
start_mappers()


# TODO: Probably redundant factory method
def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    return app
