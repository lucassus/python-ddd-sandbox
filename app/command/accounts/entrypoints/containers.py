from dependency_injector import containers, providers

from app.command.accounts.application.authentication import Authentication
from app.command.accounts.application.change_user_email_address import ChangeUserEmailAddress
from app.command.accounts.application.register_user import RegisterUser
from app.command.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.command.shared_kernel.message_bus import MessageBus
from app.infrastructure.db import AppSession


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[".endpoints"],
        auto_wire=False,
    )

    bus = providers.Dependency(instance_of=MessageBus)
    uow = providers.Factory(UnitOfWork, session_factory=lambda: AppSession())
    jwt_secret_key = providers.Dependency(instance_of=str)

    register_user = providers.Factory(RegisterUser, uow=uow, bus=bus)
    authenticate = providers.Factory(Authentication, uow=uow, jwt_secret_key=jwt_secret_key)
    change_user_email_address = providers.Factory(ChangeUserEmailAddress, uow=uow)
