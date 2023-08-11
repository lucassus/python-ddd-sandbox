import abc
from typing import Optional

from app.command.accounts.application.queries import schemas
from app.command.shared_kernel.query import Query


class AbstractFindUserQuery(Query):
    @abc.abstractmethod
    def __call__(self, *, id: int) -> Optional[schemas.UserDetails]:
        raise NotImplementedError()
