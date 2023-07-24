from sqlalchemy import select

from app.infrastructure.tables import projects_table, users_table
from app.query.queries.abstract_query import AbstractQuery


# TODO: Join projects
class FindUserQuery(AbstractQuery):
    def __call__(self, *, id: int):
        query = users_table.outerjoin(projects_table).select().where(users_table.c.id == id)
        # query = (
        #     select([users_table])
        #     .where(users_table.c.id == id)
        #     .outerjoin(projects_table)
        # )
        print(query)
        return self._database.fetch_one(query)
