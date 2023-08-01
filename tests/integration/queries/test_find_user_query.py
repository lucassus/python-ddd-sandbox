from app.query.queries.users import FindUserQuery


def test_find_user_query(connection, create_user, create_project):
    user = create_user()
    create_project(user=user, name="Project One")
    create_project(user=user, name="Project Two")

    find_user = FindUserQuery(connection=connection)
    loaded = find_user(id=user.id)

    assert loaded
    assert loaded.id == user.id
    assert loaded.email == "test@email.com"
    assert len(loaded.projects) == 2


def test_find_user_query_not_found(connection):
    find_user = FindUserQuery(connection=connection)
    user = find_user(id=1)

    assert user is None
