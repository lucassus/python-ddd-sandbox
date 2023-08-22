from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.modules.errors_handling import register_error_handlers
from app.modules.event_handlers import bus

mapper_registry = registry()


def create_app() -> FastAPI:
    from app.modules.accounts.register_module import register_module as register_accounts_module
    from app.modules.projects.register_module import register_module as register_projects_module

    app = FastAPI()

    accounts_container = register_accounts_module(app, mapper_registry, bus)
    projects_container = register_projects_module(app, mapper_registry)

    # Pass down assembled authentication service to comply with the contract
    projects_container.application.authentication.override(
        providers.Factory(accounts_container.application.authentication),
    )

    register_error_handlers(app)

    return app
