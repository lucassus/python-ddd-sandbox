from sqlalchemy.orm import mapper

from todos.infrastructure.tables import users_table
from todos.services.accounts.domain.entities import User


def start_mappers():
    mapper(User, users_table)
