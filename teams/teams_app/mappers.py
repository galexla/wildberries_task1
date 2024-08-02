import dataclasses

from core.entities import Member as MemberEntity
from core.entities import Team as TeamEntity

from .models import Member, Team


class MemberMapper:
    @classmethod
    def to_domain(cls, instance: Member) -> MemberEntity:
        team_id = (
            str(instance.team_id) if instance.team_id is not None else None
        )
        entity: MemberEntity = MemberEntity(
            id=str(instance.id),
            name=instance.name,
            position=instance.position,
            team_id=team_id,
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


def dataclass_from_dict(klass, d):
    try:
        fieldtypes = {f.name: f.type for f in dataclasses.fields(klass)}
        return klass(
            **{f: dataclass_from_dict(fieldtypes[f], d[f]) for f in d}
        )
    except:
        return d
