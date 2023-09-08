from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.modules.errors_handling import register_error_handlers
from app.shared.dependencies import get_authentication, get_message_bus
from app.shared.message_bus import MessageBus

mapper_registry = registry()

bus = MessageBus()


def create_app() -> FastAPI:
    from app.modules.accounts.bootstrap import bootstrap_accounts_module
    from app.modules.projects.bootstrap import bootstrap_projects_module

    accounts_container = bootstrap_accounts_module(mapper_registry, bus)
    bootstrap_projects_module(mapper_registry, bus)

    # Include routers
    from app.modules.accounts.entrypoints.routes import router as accounts_router
    from app.modules.projects.entrypoints.routes import router as projects_router

    app = FastAPI()

    app.dependency_overrides[get_message_bus] = lambda: bus
    app.dependency_overrides[get_authentication] = lambda: accounts_container.authentication()

    app.include_router(accounts_router)
    app.include_router(projects_router)

    register_error_handlers(app)

    return app
