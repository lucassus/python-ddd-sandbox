from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from todos.common.errors import EntityNotFoundError
from todos.infrastructure.session import session_factory
from todos.services.accounts.domain.entities import User
from todos.services.accounts.entrypoints.routes import api_router as api_router_2
from todos.services.message_bus import bus
from todos.services.project_management.adapters.unit_of_work import UnitOfWork
from todos.services.project_management.domain.service import Service
from todos.services.project_management.entrypoints.routes import (
    api_router as api_router_1,
)


# TODO: Figure out how to refactor it
def start_mappers():
    from todos.services.accounts.adapters.mappers import (
        start_mappers as start_accounts_mappers,
    )
    from todos.services.project_management.adapters.mappers import (
        start_mappers as start_project_management_mappers,
    )

    start_accounts_mappers()
    start_project_management_mappers()


start_mappers()


# TODO: Find a better place for attaching events
@bus.listen(User.AccountCreatedEvent)
def create_example_project(event: User.AccountCreatedEvent):
    uow = UnitOfWork(session_factory=session_factory)
    service = Service(uow=uow)

    return service.create_example_project(user_id=event.user_id)


def create_app() -> FastAPI:
    app = FastAPI()

    # TODO: Figure out how to refactor it
    app.include_router(api_router_1)
    app.include_router(api_router_2)

    @app.exception_handler(EntityNotFoundError)
    async def unicorn_exception_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )

    return app
