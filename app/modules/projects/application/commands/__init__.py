from app.modules.projects.application.commands.archive_project import ArchiveProject, ArchiveProjectHandler
from app.modules.projects.application.commands.complete_task import CompleteTask, CompleteTaskHandler
from app.modules.projects.application.commands.create_example_project import (
    CreateExampleProject,
    CreateExampleProjectHandler,
)
from app.modules.projects.application.commands.create_project import CreateProject, CreateProjectHandler
from app.modules.projects.application.commands.create_task import CreateTask, CreateTaskHandler
from app.modules.projects.application.commands.delete_project import DeleteProject, DeleteProjectHandler
from app.modules.projects.application.commands.incomplete_task import IncompleteTask, IncompleteTaskHandler
from app.modules.projects.application.commands.unarchive_project import UnarchiveProject, UnarchiveProjectHandler
from app.modules.projects.application.commands.update_project import UpdateProject, UpdateProjectHandler

__all__ = [
    "ArchiveProject",
    "ArchiveProjectHandler",
    "CompleteTask",
    "CompleteTaskHandler",
    "CreateExampleProject",
    "CreateExampleProjectHandler",
    "CreateProject",
    "CreateProjectHandler",
    "CreateTask",
    "CreateTaskHandler",
    "DeleteProject",
    "DeleteProjectHandler",
    "IncompleteTask",
    "IncompleteTaskHandler",
    "UnarchiveProject",
    "UnarchiveProjectHandler",
    "UpdateProject",
    "UpdateProjectHandler",
]
