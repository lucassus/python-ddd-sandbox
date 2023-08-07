from app.command.projects.application.specifications import ActiveProjectSpecification
from app.command.projects.entities.project_builder import ProjectBuilder
from app.utc_datetime import utc_now


class TestActiveProjectSpecification:
    def test_returns_true_for_archived_projects(self):
        spec = ActiveProjectSpecification()
        project = ProjectBuilder().build()

        assert spec.is_satisfied_by(project) is True

    def test_returns_false_for_archived_projects(self):
        spec = ActiveProjectSpecification()
        project = ProjectBuilder().build()
        project.archive(now=utc_now())

        assert spec.is_satisfied_by(project) is False

    def test_returns_false_for_deleted_projects(self):
        spec = ActiveProjectSpecification()
        project = ProjectBuilder().build()
        project.archive(now=utc_now())
        project.delete(now=utc_now())

        assert spec.is_satisfied_by(project) is False
