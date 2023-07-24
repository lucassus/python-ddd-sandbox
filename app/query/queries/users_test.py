from app.infrastructure.tables import projects_table, users_table
from app.query.queries.users import FindUserQuery


def test_find_user_query(connection):
    connection.execute(
        users_table.insert(),
        [{"id": 1, "email": "test@email.com", "password": "password"}],
    )

    assert connection.execute(
        projects_table.insert(),
        [
            {"user_id": 1, "name": "Project One"},
            {"user_id": 1, "name": "Project Two"},
        ],
    )

    find_user = FindUserQuery(connection=connection)
    user = find_user(id=1)

    assert user


def test_find_user_query_not_found(connection):
    find_user = FindUserQuery(connection=connection)
    user = find_user(id=1)

    assert user is None
