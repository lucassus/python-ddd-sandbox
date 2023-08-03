from fastapi import FastAPI
from sqlalchemy.orm import registry


def register_module(app: FastAPI, mappers: registry) -> None:
    from app.command.accounts.entrypoints.routes import router
    from app.command.accounts.infrastructure.mappers import start_mappers

    start_mappers(mappers)
    app.include_router(router)
