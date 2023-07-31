from app.command.projects.application.create_example_project import CreateExampleProject
from app.command.projects.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.shared_kernel.user_id import UserID


def test_create_example_project(fake_uow: FakeUnitOfWork):
    create_example_project = CreateExampleProject(uow=fake_uow)
    project_id = create_example_project(user_id=UserID(1))

    assert fake_uow.committed

    project = fake_uow.project.get(project_id)
    assert project.name == "My first project"
    assert project.user_id == UserID(1)
    assert len(project.tasks) == 3
    assert project.tasks[0].name == "Sign up!"
    assert project.tasks[0].completed_at is not None
    assert project.tasks[1].name == "Watch the tutorial"
    assert project.tasks[2].name == "Start using our awesome app"
