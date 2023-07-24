from app.query.factories import create_project, create_user
from app.query.queries.users import FindUserQuery


def test_find_user_query(connection):
    user_id = create_user(connection, email="test@email.com").id
    create_project(connection, user_id=user_id, name="Project One")
    create_project(connection, user_id=user_id, name="Project Two")

    find_user = FindUserQuery(connection=connection)
    user = find_user(id=user_id)

    assert user
    assert user.id == user_id
    assert user.email == "test@email.com"
    assert len(user.projects) == 2


def test_find_user_query_not_found(connection):
    find_user = FindUserQuery(connection=connection)
    user = find_user(id=1)

    assert user is None
