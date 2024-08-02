from core.services import MemberService, TeamService
from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .repositories import MemberRepositoryImpl, TeamRepositoryImpl

memberRepository = MemberRepositoryImpl()
memberService = MemberService(memberRepository)

teamRepository = TeamRepositoryImpl()
teamService = TeamService(teamRepository)


class MemberIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(validators=[MinValueValidator(1)])

    def validate_id(self, value: int) -> int:
        member = memberService.get_by_id(value)
        if not member:
            raise ValidationError(f"Member with id {value} does not exist")
        return value


class MemberSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=False, validators=[MinValueValidator(1)]
    )
    name = serializers.CharField(max_length=400, allow_blank=False)
    position = serializers.CharField(max_length=400, allow_blank=False)
    team_id = serializers.IntegerField(
        required=False, validators=[MinValueValidator(1)]
    )

    def validate_id(self, value: int) -> int:
        member = memberService.get_by_id(value)
        if not member:
            raise ValidationError(f"Member with id {value} does not exist")
        return value

    def validate_team_id(self, value: int) -> int:
        team = teamService.get_by_id(value)
        if not team:
            raise ValidationError(f"Team with id {value} does not exist")
        return value


class TeamIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(validators=[MinValueValidator(1)])

    def validate_id(self, value: int) -> int:
        team = teamService.get_by_id(value)
        if not team:
            raise ValidationError(f"Team with id {value} does not exist")
        return value


class TeamSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=False, validators=[MinValueValidator(1)]
    )
    name = serializers.CharField(max_length=400, allow_blank=False)

    def validate_id(self, value: int) -> int:
        team = teamService.get_by_id(value)
        if not team:
            raise ValidationError(f"Team with id {value} does not exist")
        return value
