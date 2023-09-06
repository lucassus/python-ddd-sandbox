from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry


from app.modules.errors_handling import register_error_handlers
from app.modules.event_handlers import bus


mapper_registry = registry()


def create_app() -> FastAPI:
    from app.modules.accounts.bootstrap import bootstrap_accounts_module
    from app.modules.projects.bootstrap import bootstrap_projects_module

    app = FastAPI()

    accounts_container = bootstrap_accounts_module(app, mapper_registry, bus)
    projects_container = bootstrap_projects_module(app, mapper_registry, bus)

    # Pass down assembled authentication service to comply with the contract
    projects_container.application.authentication.override(
        providers.Factory(accounts_container.application.authentication),
    )

    register_error_handlers(app)

    return app
