from sqlalchemy.orm import mapper

from examples.user import User
from todos.infrastructure.tables import users_table


def start_mappers():
    mapper(User, users_table)
