import abc

from app.modules.projects.domain.project import Project, ProjectID


class AbstractProjectRepository(abc.ABC):
    _seen: set[Project]

    def __init__(self):
        self._seen = set()

    @property
    def seen(self) -> frozenset[Project]:
        return frozenset(self._seen)

    def create(self, project: Project) -> Project:
        project = self._create(project)
        self._seen.add(project)
        return project

    def get(self, id: ProjectID) -> Project:
        project = self._get(id)

        if project is not None:
            self._seen.add(project)

        return project

    def get_archived(self, id: ProjectID) -> Project:
        project = self._get_archived(id)

        if project is not None:
            self._seen.add(project)

        return project

    # User repository uses a composition for address a problem with ugly _* methods

    @abc.abstractmethod
    def _create(self, project: Project) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id: ProjectID) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_archived(self, id: ProjectID) -> Project:
        raise NotImplementedError
