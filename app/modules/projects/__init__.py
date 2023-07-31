from fastapi import FastAPI
from sqlalchemy.dialects import registry


def register_module(app: FastAPI, mappers: registry) -> None:
    from app.modules.projects.entrypoints.adapters.mappers import start_mappers
    from app.modules.projects.entrypoints.routes import router

    start_mappers(mappers)
    app.include_router(router)
