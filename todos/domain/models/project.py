from dataclasses import dataclass
from typing import Optional


@dataclass
class Project:
    name: str
    id: Optional[int] = None
