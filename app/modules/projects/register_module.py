from fastapi import FastAPI
from sqlalchemy.orm import registry

from app import engine


def register_module(app: FastAPI, mappers: registry) -> None:
    from app.modules.projects.entrypoints import routes
    from app.modules.projects.entrypoints.containers import Container
    from app.modules.projects.infrastructure.mappers import start_mappers

    container = Container(engine=engine)
    container.wire()

    start_mappers(mappers)
    app.include_router(routes.router)