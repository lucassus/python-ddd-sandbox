from dataclasses import dataclass, field
from datetime import datetime
from typing import NewType, Optional

from app.command.shared_kernel.entity import Entity

TaskNumber = NewType("TaskNumber", int)


@dataclass(kw_only=True)
class Task(Entity):
    number: TaskNumber = field(init=False)
    name: str
    completed_at: Optional[datetime] = None

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    def complete(self, now: datetime) -> None:
        if not self.is_completed:
            self.completed_at = now

    def incomplete(self) -> None:
        if self.is_completed:
            self.completed_at = None
