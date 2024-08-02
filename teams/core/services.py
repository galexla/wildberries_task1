import dataclasses

from .entities import Member, Team
from .repositories import MemberRepository, TeamRepository


def to_dict_list(objects: list[dataclasses.dataclass]):
    return [dataclasses.asdict(elem) for elem in objects]


class MemberService:
    def __init__(self, member_repository: MemberRepository) -> None:
        self.member_repository = member_repository

    def get_list(self) -> list[Member]:
        return self.member_repository.get_list()

    def create(self, name: str, position: str, team_id=None) -> Member:
        return self.member_repository.create(name, position, team_id)

    def update(self, id, **kwargs) -> bool:
        return self.member_repository.update(id, **kwargs)

    def get_by_id(self, id) -> Member:
        return self.member_repository.get_by_id(id)

    def set_team_id(self, id, team_id) -> None:
        return self.member_repository.set_team_id(id, team_id)

    def remove(self, id) -> None:
        return self.member_repository.remove(id)


class TeamService:
    def __init__(self, team_repository: TeamRepository) -> None:
        self.team_repository = team_repository

    def get_list(self) -> list[Team]:
        return self.team_repository.get_list()

    def create(self, name: str) -> Team:
        return self.team_repository.create(name)

    def update(self, id, **kwargs) -> bool:
        return self.team_repository.update(id, **kwargs)

    def get_by_id(self, id) -> Team:
        return self.team_repository.get_by_id(id)

    def remove(self, id) -> None:
        return self.team_repository.remove(id)
