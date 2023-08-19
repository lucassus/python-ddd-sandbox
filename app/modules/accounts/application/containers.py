from dependency_injector import containers, providers

from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.change_user_email_address import ChangeUserEmailAddress
from app.modules.accounts.application.jwt import JWT
from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.application.register_user import RegisterUser
from app.modules.shared_kernel.message_bus import MessageBus


class ApplicationContainer(containers.DeclarativeContainer):
    bus = providers.Dependency(instance_of=MessageBus)

    jwt_secret_key = providers.Dependency(instance_of=str)
    jwt = providers.Singleton(JWT, secret_key=jwt_secret_key)

    uow = providers.AbstractFactory(AbstractUnitOfWork)

    register_user = providers.Singleton(RegisterUser, uow=uow, bus=bus)
    authentication = providers.Singleton(Authentication, uow=uow, jwt=jwt)
    change_user_email_address = providers.Singleton(ChangeUserEmailAddress, uow=uow)
