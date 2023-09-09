import pytest

from app.anys import AnyUUID
from app.infrastructure.db import engine
from app.modules.accounts.queries.get_user_query import GetUserQuery
from app.modules.shared_kernel.entities.user_id import UserID


def test_get_user_query(create_user, create_project):
    user = create_user()
    create_project(user=user, name="Project One")
    create_project(user=user, name="Project Two")

    get_user = GetUserQuery(engine=engine)
    loaded = get_user(id=user.id)

    assert loaded
    assert loaded.id == AnyUUID
    assert loaded.email == "test@email.com"
    assert len(loaded.projects) == 2


def test_find_user_query_not_found():
    find_user = GetUserQuery(engine=engine)

    with pytest.raises(GetUserQuery.NotFoundError):
        find_user(id=UserID.generate())
