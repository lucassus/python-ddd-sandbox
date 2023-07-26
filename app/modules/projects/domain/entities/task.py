from dataclasses import dataclass
from datetime import date
from typing import NewType, Optional

from app.shared_kernel.base_entity import BaseEntity

TaskID = NewType("TaskID", int)


@dataclass
class Task(BaseEntity[TaskID]):
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
