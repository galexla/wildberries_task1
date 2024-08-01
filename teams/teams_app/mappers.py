from core.entities import Member as MemberEntity
from core.entities import Team as TeamEntity

from .models import Member, Team


class MemberMapper:
    @classmethod
    def to_domain(cls, instance: Member) -> MemberEntity:
        entity: MemberEntity = MemberEntity(
            id=instance.id, name=instance.name, position=instance.position
        )
        return entity

    @classmethod
    def to_entity(cls, member: MemberEntity): ...


class TeamMapper:
    @classmethod
    def to_domain(cls, instance: Team) -> TeamEntity:
        members = [str(m.id) for m in instance.members.all()]
        entity: TeamEntity = TeamEntity(
            id=instance.id, name=instance.name, members=members
        )
        return entity

    @classmethod
    def to_entity(cls, team: TeamEntity): ...
