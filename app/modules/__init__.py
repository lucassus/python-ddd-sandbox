from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.modules.errors_handling import register_error_handlers
from app.shared.message_bus import MessageBus

# TODO: Find a way to make it private
mapper_registry = registry()

# TODO: Find a way to make it private
bus = MessageBus()


def create_app() -> FastAPI:
    app = FastAPI()

    from app.modules.accounts.bootstrap import bootstrap_accounts_module
    from app.modules.projects.bootstrap import bootstrap_projects_module

    authentication = bootstrap_accounts_module(mapper_registry, bus)
    # Pass down assembled authentication service to comply with the contract
    bootstrap_projects_module(mapper_registry, bus, authentication)

    # Include routers
    from app.modules.accounts.entrypoints.routes import router as accounts_router
    from app.modules.projects.entrypoints.routes import router as projects_router

    app.include_router(accounts_router)
    app.include_router(projects_router)

    register_error_handlers(app)

    return app
