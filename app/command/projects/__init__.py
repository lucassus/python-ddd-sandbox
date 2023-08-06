from fastapi import FastAPI
from sqlalchemy.orm import registry


def register_module(app: FastAPI, mappers: registry) -> None:
    from app.command.projects.entrypoints import endpoints
    from app.command.projects.entrypoints.containers import Container
    from app.command.projects.infrastructure.mappers import start_mappers

    container = Container()
    container.wire(
        modules=[
            ".entrypoints.endpoints.project_tasks",
            ".entrypoints.endpoints.projects",
        ]
    )

    start_mappers(mappers)
    app.include_router(endpoints.router)
