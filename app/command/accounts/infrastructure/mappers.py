from app.command.accounts.entities.user import User
from app.infrastructure.tables import users_table


def start_mappers(mapper_registry):
    mapper_registry.map_imperatively(
        User,
        users_table,
        properties={
            "_id": users_table.c.id,
            "_email": users_table.c.email,
            "_password": users_table.c.password,
        },
    )
