from dependency_injector import providers
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import registry

from app.modules.authentication_contract import AuthenticationError
from app.modules.event_handlers import bus
from app.modules.shared_kernel.errors import EntityNotFoundError

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

    # TODO: Figure out how to test these handlers
    # TODO: This should also handle errors from queries
    @app.exception_handler(EntityNotFoundError)
    def handle_entity_not_found_error(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    # TODO: Improve this idea
    @app.exception_handler(AuthenticationError)
    def handler_authentication_error(request: Request, exc: AuthenticationError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    return app
