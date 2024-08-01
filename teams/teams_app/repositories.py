from core.entities import Member as MemberEntity
from core.entities import Team as TeamEntity
from core.repositories import MemberRepository, TeamRepository

from .mappers import MemberMapper, TeamMapper
from .models import Member, Team


class MemberRepositoryImpl(MemberRepository):
    def create(self, name: str, position: str) -> MemberEntity:
        instance = Member.objects.create(name=name, position=position)
        return MemberMapper.to_domain(instance)

    def get_by_id(self, id) -> MemberEntity | None:
        instance = Member.objects.filter(id=id).first()
        if instance is None:
            return None
        return MemberMapper.to_domain(instance)

    def remove(self, id) -> None:
        Member.objects.filter(id=id).delete()


class TeamRepositoryImpl(TeamRepository):
    def create(self, name: str) -> TeamEntity:
        instance = Team.objects.create(name=name)
        return TeamMapper.to_domain(instance)

    def get_by_id(self, id) -> TeamEntity | None:
        instance = Team.objects.filter(id=id).first()
        if instance is None:
            return None
        return TeamMapper.to_domain(instance)

    def add_member(self, id, member_id) -> None:
        Member.objects.filter(id=member_id).update(team_id=id)

    def add_members(self, id, member_ids: list) -> None:
        Member.objects.filter(id__in=member_ids).update(team_id=id)

    def remove_member(self, id, member_id) -> None:
        Member.objects.filter(team_id=id, id=member_id).update(team_id=None)

    def remove_members(self, id, member_ids: list) -> None:
        Member.objects.filter(team_id=id, id__in=member_ids).update(
            team_id=None
        )

    def remove(self, id) -> None:
        Team.objects.filter(id=id).delete()
