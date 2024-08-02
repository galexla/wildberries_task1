from core.entities import Member as MemberEntity
from core.entities import Team as TeamEntity
from core.repositories import MemberRepository, TeamRepository

from .mappers import MemberMapper, TeamMapper
from .models import Member, Team


class MemberRepositoryImpl(MemberRepository):
    def get_list(self) -> list[MemberEntity]:
        queryset = Member.objects.all()
        return [MemberMapper.to_domain(member) for member in queryset]

    def create(self, name: str, position: str, team_id=None) -> MemberEntity:
        instance = Member.objects.create(
            name=name, position=position, team_id=team_id
        )
        return MemberMapper.to_domain(instance)

    def update(self, id, **kwargs) -> None:
        queryset = Member.objects.filter(id=id)
        queryset.update(**kwargs)

    def get_by_id(self, id) -> MemberEntity | None:
        instance = Member.objects.filter(id=id).first()
        if instance is None:
            return None
        return MemberMapper.to_domain(instance)

    def set_team_id(self, id, team_id) -> None:
        instance = Member.objects.filter(id=id).first()
        instance.team_id = team_id
        instance.save()

    def remove(self, id) -> None:
        Member.objects.filter(id=id).delete()


class TeamRepositoryImpl(TeamRepository):
    def get_list(self) -> list[TeamEntity]:
        teams = Team.objects.all()
        return [TeamMapper.to_domain(team) for team in teams]

    def create(self, name: str) -> TeamEntity:
        instance = Team.objects.create(name=name)
        return TeamMapper.to_domain(instance)

    def update(self, id, **kwargs) -> None:
        instance = Team.objects.filter(id=id)
        instance.update(**kwargs)

    def get_by_id(self, id) -> TeamEntity | None:
        instance = Team.objects.filter(id=id).first()
        if instance is None:
            return None
        return TeamMapper.to_domain(instance)

    def remove(self, id) -> None:
        Team.objects.filter(id=id).delete()
