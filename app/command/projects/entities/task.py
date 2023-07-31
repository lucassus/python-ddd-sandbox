from dataclasses import dataclass, field
from datetime import date
from typing import NewType, Optional

from app.shared_kernel.entity import Entity

TaskNumber = NewType("TaskNumber", int)


@dataclass
class Task(Entity):
    number: TaskNumber = field(init=False)
    name: str
    completed_at: Optional[date] = None

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    def complete(self, now: date) -> None:
        if not self.is_completed:
            self.completed_at = now

    def incomplete(self) -> None:
        if self.is_completed:
            self.completed_at = None
