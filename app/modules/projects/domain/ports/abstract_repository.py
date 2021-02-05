import abc
from typing import List

from app.common.base_repository import BaseRepository
from app.modules.projects.domain.entities import Project


class AbstractRepository(BaseRepository[Project]):
    @abc.abstractmethod
    def list(self) -> List[Project]:
        raise NotImplementedError
