from app.infrastructure.tables import projects_table, users_table
from app.query.queries.users import FindUserQuery


def test_find_user_query(connection):
    # TODO: Figure out how to create factories for this
    result = connection.execute(
        users_table.insert()
        .values(
            {"email": "test@email.com", "password": "password"},
        )
        .returning(users_table.c.id),
    )

    user_id = result.fetchone().id

    connection.execute(
        projects_table.insert()
        .values(
            [
                {"user_id": user_id, "name": "Project One"},
                {"user_id": user_id, "name": "Project Two"},
            ]
        )
        .returning(projects_table.c.id),
    )

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
