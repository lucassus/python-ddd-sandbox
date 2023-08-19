import pytest
from sqlalchemy import Connection

from app.modules.accounts.queries.find_user_query import GetUserQuery
from app.modules.shared_kernel.entities.user_id import UserID


def test_get_user_query(connection: Connection, create_user, create_project):
    user = create_user()
    create_project(user=user, name="Project One")
    create_project(user=user, name="Project Two")

    get_user = GetUserQuery(connection=connection)
    loaded = get_user(id=user.id)

    assert loaded
    assert loaded.id == user.id
    assert loaded.email == "test@email.com"
    assert len(loaded.projects) == 2


def test_find_user_query_not_found(connection: Connection):
    find_user = GetUserQuery(connection=connection)

    with pytest.raises(GetUserQuery.NotFoundError):
        find_user(id=UserID(1))
