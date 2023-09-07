from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.infrastructure.message_bus import MessageBus
from app.modules.errors_handling import register_error_handlers

mapper_registry = registry()

# TODO: Bit better, but still smelly
_bus: MessageBus | None = None


def get_bus() -> MessageBus:
    global _bus

    if _bus is None:
        _bus = MessageBus()

    return _bus


def create_app() -> FastAPI:
    app = FastAPI()
    bus = get_bus()

    from app.modules.accounts.bootstrap import bootstrap_accounts_module
    from app.modules.projects.bootstrap import bootstrap_projects_module

    accounts_container = bootstrap_accounts_module(mapper_registry, bus)
    projects_container = bootstrap_projects_module(mapper_registry, bus)

    # Pass down assembled authentication service to comply with the contract
    projects_container.application.authentication.override(
        providers.Factory(accounts_container.application.authentication),
    )

    # Include routers
    from app.modules.accounts.entrypoints.routes import router as accounts_router
    from app.modules.projects.entrypoints.routes import router as projects_router

    app.include_router(accounts_router)
    app.include_router(projects_router)

    register_error_handlers(app)

    return app
