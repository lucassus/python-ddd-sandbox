from dataclasses import dataclass
from typing import Optional

from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.message_bus import Command, CommandHandler


@dataclass(frozen=True)
class CreateTask(Command[TaskNumber]):
    project_id: ProjectID
    name: str
    created_by: Optional[UserID] = None


class CreateTaskHandler(CommandHandler[CreateTask, TaskNumber]):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: CreateTask) -> TaskNumber:
        with self.uow:
            project = self.uow.projects.get(command.project_id)

            name, created_by = command.name, command.created_by
            task = project.add_task(name, created_by)
            self.uow.commit()

            return task.number
