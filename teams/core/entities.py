import dataclasses


@dataclasses.dataclass
class Member:
    id: str
    name: str
    position: str
    team_id: str


@dataclasses.dataclass
class Team:
    id: str
    name: str
    members: list[str]
