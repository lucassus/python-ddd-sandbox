import pytest

from app.infrastructure.tables import projects_table, users_table
from app.query.queries.users import FindUserQuery


@pytest.mark.asyncio
async def test_find_user_query(database):
    await database.execute(
        query=users_table.insert(),
        values={"id": 1, "email": "test@email.com", "password": "password"},
    )

    assert database.execute(
        query=projects_table.insert(),
        values=[
            {"user_id": 1, "name": "Project One"},
            {"user_id": 1, "name": "Project Two"},
        ],
    )

    find_user = FindUserQuery(database=database)
    user = await find_user(id=1)

    assert user
