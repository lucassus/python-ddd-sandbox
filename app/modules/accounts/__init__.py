from fastapi import FastAPI
from sqlalchemy.orm import registry


def register_module(app: FastAPI, mappers: registry) -> None:
    from app.modules.accounts.adapters.mappers import start_mappers
    from app.modules.accounts.entrypoints.routes import router

    start_mappers(mappers)
    app.include_router(router)
