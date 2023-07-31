from app.command.accounts.domain import User
from app.infrastructure.tables import users_table


def start_mappers(mapper_registry):
    mapper_registry.map_imperatively(User, users_table)
