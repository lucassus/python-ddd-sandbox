from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app import engine
from app.modules.authentication_contract import AuthenticationContract


def register_module(
    app: FastAPI,
    mappers: registry,
    authentication: AuthenticationContract,
) -> None:
    from app.modules.projects.entrypoints import routes
    from app.modules.projects.entrypoints.containers import Container
    from app.modules.projects.infrastructure.mappers import start_mappers

    container = Container(
        engine=engine,
        authentication=providers.Object(authentication),
    )
    container.wire()

    start_mappers(mappers)
    app.include_router(routes.router)
