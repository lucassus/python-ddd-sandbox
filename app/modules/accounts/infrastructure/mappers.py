from sqlalchemy import event

from app.infrastructure.tables import users_table
from app.modules.accounts.domain.user import User


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

    # Because SQLAlchemy doesn't call a constructor when loading an object from the database.
    @event.listens_for(User, "load")
    def receive_load(user, _):
        user._events = []
