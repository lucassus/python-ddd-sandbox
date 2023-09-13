import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from app.infrastructure.tables import users_table


async def async_main() -> None:
    engine = create_async_engine(
        "sqlite+aiosqlite:///app/infrastructure/databases/development.db",
        echo=True,
    )

    async with engine.connect() as conn:
        stmt = select(users_table.c.id, users_table.c.email).select_from(users_table)
        result = await conn.execute(stmt)

        print(result.fetchall())

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
