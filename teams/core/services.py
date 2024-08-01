from .entities import Member, Team
from .repositories import MemberRepository, TeamRepository


class MemberService:
    def __init__(self, member_repository: MemberRepository) -> None:
        self.member_repository = member_repository

    def create(self, name: str, position: str) -> Member:
        return self.member_repository.create(name, position)

    def get_by_id(self, id) -> Member:
        return self.member_repository.get_by_id(id)

    def remove(self, id) -> None:
        self.member_repository.remove(id)


class TeamService:
    def __init__(self, team_repository: TeamRepository) -> None:
        self.team_repository = team_repository

    def create(self, name: str) -> Team:
        return self.team_repository.remove(id)

    def get_by_id(self, id) -> Team:
        return self.team_repository.get_by_id(id)

    def add_member(self, member_id) -> None:
        self.team_repository.add_member(member_id)

    def add_members(self, member_ids: list) -> None:
        self.team_repository.remove(member_ids)

    def remove_member(self, member_id) -> None:
        self.team_repository.remove_member(member_id)

    def remove_members(self, member_ids: list) -> None:
        return self.team_repository.remove_members(member_ids)

    def remove(self, id) -> None:
        return self.team_repository.remove(id)
