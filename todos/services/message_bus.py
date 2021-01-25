from todos.common.message_bus import MessageBus
from todos.infrastructure.session import session_factory
from todos.services.accounts.domain.entities import User
from todos.services.project_management.adapters.unit_of_work import UnitOfWork
from todos.services.project_management.domain.service import Service

bus = MessageBus()


@bus.listen(User.AccountCreatedEvent)
def handle_create_example_project(event: User.AccountCreatedEvent):
    uow = UnitOfWork(session_factory=session_factory)
    service = Service(uow=uow)

    return service.create_example_project(user_id=event.user_id)
