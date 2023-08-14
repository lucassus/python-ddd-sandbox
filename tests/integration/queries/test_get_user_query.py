import pytest

from app.modules.accounts.application.queries.find_user_query import GetUserQueryError
from app.modules.accounts.infrastructure.queries.find_user_query import GetUserSQLQuery
from app.modules.shared_kernel.entities.user_id import UserID


def test_get_user_query(connection, create_user, create_project):
    user = create_user()
    create_project(user=user, name="Project One")
    create_project(user=user, name="Project Two")

    find_user = GetUserSQLQuery(connection=connection)
    loaded = find_user(id=user.id)

    assert loaded
    assert loaded.id == user.id
    assert loaded.email == "test@email.com"
    assert len(loaded.projects) == 2


def test_find_user_query_not_found(connection):
    find_user = GetUserSQLQuery(connection=connection)

    with pytest.raises(GetUserQueryError):
        find_user(id=UserID(1))
