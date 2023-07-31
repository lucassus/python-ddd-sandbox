from fastapi import FastAPI

from app.command.app import create_app as create_commands_app
from app.infrastructure.db import engine
from app.infrastructure.tables import create_tables
from app.query.app import create_app as create_queries_app


def create_app():
    create_tables(engine)

    app = FastAPI()

    app.mount("/queries", create_queries_app())
    app.mount("/commands", create_commands_app())

    return app
