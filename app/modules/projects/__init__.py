from fastapi import FastAPI
from sqlalchemy.dialects import registry

from app.modules.projects.adapters.unit_of_work import UnitOfWork  # noqa
from app.modules.projects.domain.use_cases.create_example_project import CreateExampleProject  # noqa


def register_module(app: FastAPI, mappers: registry) -> None:
    from app.modules.projects.adapters.mappers import start_mappers
    from app.modules.projects.entrypoints.routes import router

    start_mappers(mappers)
    app.include_router(router)
