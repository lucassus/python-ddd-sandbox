from app.infrastructure.tables import users_table
from app.query.queries.abstract_query import AbstractQuery


class FindUserQuery(AbstractQuery):
    def __call__(self, *, id: int):
        query = users_table.select().where(users_table.c.id == id)

        result = self._connection.execute(query)
        return result.first()
