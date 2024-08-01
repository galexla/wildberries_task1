import dataclasses


@dataclasses.dataclass
class Member:
    id: str
    name: str
    position: str


@dataclasses.dataclass
class Team:
    id: str
    name: str
    members: list[str]
