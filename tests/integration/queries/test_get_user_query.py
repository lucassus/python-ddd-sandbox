import pytest

from app.anys import AnyUUID
from app.infrastructure.db import async_engine
from app.modules.accounts.application.queries import GetUser
from app.modules.accounts.infrastructure.queries import GetUserQueryHandler
from app.modules.shared_kernel.entities.user_id import UserID


class TestGetUserQueryHandler:
    @pytest.fixture()
    def handler(self):
        return GetUserQueryHandler(engine=async_engine)

    @pytest.mark.asyncio()
    async def test_it_loads_user_details(
        self,
        create_user,
        create_project,
        handler: GetUserQueryHandler,
    ):
        user = create_user()
        create_project(user=user, name="Project One")
        create_project(user=user, name="Project Two")

        loaded = await handler(GetUser(user.id))

        assert loaded
        assert loaded.id == AnyUUID
        assert loaded.email == "test@email.com"
        assert len(loaded.projects) == 2

    @pytest.mark.asyncio()
    async def test_not_found(
        self,
        handler: GetUserQueryHandler,
    ):
        with pytest.raises(GetUser.NotFoundError):
            await handler(GetUser(UserID.generate()))
