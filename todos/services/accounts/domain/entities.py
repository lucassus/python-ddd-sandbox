from dataclasses import dataclass, field


@dataclass
class User:
    id: int = field(init=False)
    email: str
    password: str
