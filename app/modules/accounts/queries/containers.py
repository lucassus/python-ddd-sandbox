from dependency_injector import containers, providers
from sqlalchemy import Connection

from app.modules.accounts.queries.find_user_query import GetUserQuery


class QueriesContainer(containers.DeclarativeContainer):
    connection = providers.Dependency(instance_of=Connection)

    get_user = providers.Singleton(GetUserQuery, connection=connection)
