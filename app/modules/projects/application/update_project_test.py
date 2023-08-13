from app.modules.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.modules.projects.application.update_project import UpdateProject
from app.modules.projects.domain.project import ProjectName
from app.modules.projects.domain.project_builder import ProjectBuilder


class TestUpdateProject:
    def test_update_name(self, repository: AbstractProjectRepository, fake_uow):
        project = repository.create(ProjectBuilder().with_name(ProjectName("Old name")).build())

        update_project = UpdateProject(uow=fake_uow)
        update_project(project_id=project.id, name=ProjectName("New name"))

        updated = repository.get(project.id)
        assert updated.name == ProjectName("New name")
        assert fake_uow.committed
