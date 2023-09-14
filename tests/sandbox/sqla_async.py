import asyncio

from sqlalchemy import select

from app.infrastructure.db import async_engine
from app.infrastructure.tables import users_table


async def async_main() -> None:
    async with async_engine.connect() as conn:
        stmt = select(users_table.c.id, users_table.c.email).select_from(users_table)
        result = await conn.execute(stmt)

        print(result.fetchall())

    await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
