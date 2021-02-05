import abc

from app.common.base_repository import BaseRepository
from app.modules.accounts.domain.entities import User


class AbstractRepository(BaseRepository[User], abc.ABC):
    pass
