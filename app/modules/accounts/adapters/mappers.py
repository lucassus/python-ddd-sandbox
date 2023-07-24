from sqlalchemy.orm import mapper

from app.infrastructure.tables import users_table
from app.modules.accounts.domain.entities import User


def start_mappers(mapper_registry):
    mapper_registry.map_imperatively(User, users_table)
