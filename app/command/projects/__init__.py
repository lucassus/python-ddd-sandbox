from fastapi import FastAPI
from sqlalchemy.orm import registry


def register_module(app: FastAPI, mappers: registry) -> None:
    from app.command.projects.entrypoints import routes
    from app.command.projects.entrypoints.containers import Container
    from app.command.projects.infrastructure.mappers import start_mappers

    container = Container()
    container.wire()

    start_mappers(mappers)
    app.include_router(routes.router)
