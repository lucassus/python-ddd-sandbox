from dependency_injector import containers, providers

from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.commands import (
    ChangeUserEmailAddress,
    ChangeUserEmailAddressHandler,
    RegisterUser,
    RegisterUserHandler,
)
from app.modules.accounts.application.event_handlers import SendWelcomeEmail
from app.modules.shared_kernel.events import UserAccountCreated
from app.shared.message_bus import MessageBus


class AppContainer(containers.DeclarativeContainer):
    bus = providers.Dependency(instance_of=MessageBus)
    adapters = providers.DependenciesContainer()

    authentication = providers.Singleton(
        Authentication,
        adapters.uow,
        adapters.auth_token,
        adapters.password_hasher,
    )

    # TODO: Find more straightforward solution
    register_command_handlers = providers.Callable(
        lambda bus, command_handlers: bus.register_all(command_handlers),
        bus=adapters.bus,
        command_handlers=providers.Dict(
            {
                RegisterUser: providers.Factory(RegisterUserHandler, adapters.uow, adapters.password_hasher),
                ChangeUserEmailAddress: providers.Factory(ChangeUserEmailAddressHandler, adapters.uow),
            }
        ),
    )

    register_event_handlers = providers.Callable(
        lambda bus, event_handlers: bus.listen_all(event_handlers),
        bus=adapters.bus,
        event_handlers=providers.Dict(
            {
                UserAccountCreated: providers.List(providers.Factory(SendWelcomeEmail, adapters.uow)),
            }
        ),
    )
