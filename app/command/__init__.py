from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import registry

from app.command.event_handlers import bus
from app.command.shared_kernel.errors import EntityNotFoundError

mapper_registry = registry()


def create_app() -> FastAPI:
    from app.command.accounts.register_module import register_module as register_accounts_module
    from app.command.projects.register_module import register_module as register_projects_module

    app = FastAPI()

    register_accounts_module(app, mapper_registry, bus)
    register_projects_module(app, mapper_registry)

    # TODO: Figure out how to test these handlers
    @app.exception_handler(EntityNotFoundError)
    async def handle_entity_not_found_error(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    return app
