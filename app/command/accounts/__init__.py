from fastapi import FastAPI
from sqlalchemy.orm import registry


def register_module(app: FastAPI, mappers: registry) -> None:
    from app.command.accounts.entrypoints import endpoints
    from app.command.accounts.entrypoints.containers import Container
    from app.command.accounts.infrastructure.mappers import start_mappers

    container = Container()
    container.wire(modules=[endpoints])

    start_mappers(mappers)
    app.include_router(endpoints.router)
