from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Task:
    id: int = field(init=False)

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
