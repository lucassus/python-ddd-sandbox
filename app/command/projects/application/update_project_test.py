from app.command.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.command.projects.application.update_project import UpdateProject
from app.command.projects.entities.project import ProjectID, ProjectName
from app.command.projects.entities.project_builder import ProjectBuilder


class TestUpdateProject:
    def test_update_name(self, repository: AbstractProjectRepository, fake_uow):
        project = repository.create(ProjectBuilder().with_name(ProjectName("Old name")).build())

        update_project = UpdateProject(uow=fake_uow)
        update_project(project_id=project.id, name=ProjectName("New name"))

        updated = repository.get(project.id)
        assert updated.name == ProjectName("New name")
        assert fake_uow.committed
