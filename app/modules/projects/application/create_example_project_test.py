from app.modules.projects.application.create_example_project import CreateExampleProject
from app.modules.projects.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.shared_kernel.entities.user_id import UserID


def test_create_example_project(fake_uow: FakeUnitOfWork):
    # Given
    create_example_project = CreateExampleProject(uow=fake_uow)
    user_id = UserID.generate()

    # When
    project_id = create_example_project(user_id=user_id)

    # Then
    assert fake_uow.committed

    project = fake_uow.projects.get(project_id)
    assert project.name == "My first project"
    assert project.user_id == user_id
    assert len(project.tasks) == 3
    assert project.tasks[0].name == "Sign up!"
    assert project.tasks[0].completed_at is not None
    assert project.tasks[1].name == "Watch the tutorial"
    assert project.tasks[2].name == "Start using our awesome app"
