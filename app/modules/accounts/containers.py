from dependency_injector import containers, providers
from sqlalchemy import Engine

from app.modules.accounts.application.containers import ApplicationContainer as ApplicationContainer
from app.modules.accounts.infrastructure.containers import InfrastructureContainer
from app.modules.accounts.queries.containers import QueriesContainer
from app.modules.shared_kernel.message_bus import MessageBus


class Container(containers.DeclarativeContainer):
    bus = providers.Dependency(instance_of=MessageBus)
    engine = providers.Dependency(instance_of=Engine)
    jwt_secret_key = providers.Dependency(instance_of=str)

    infrastructure = providers.Container(InfrastructureContainer, engine=engine)

    commands = providers.Container(
        ApplicationContainer,
        jwt_secret_key=jwt_secret_key,
        bus=bus,
    )

    queries = providers.Container(
        QueriesContainer,
        connection=infrastructure.connection,
    )
