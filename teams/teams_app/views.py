from dataclasses import asdict

from core.services import MemberService, TeamService, to_dict_list
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .repositories import MemberRepositoryImpl, TeamRepositoryImpl
from .serializers import (
    MemberIdSerializer,
    MemberSerializer,
    TeamIdSerializer,
    TeamSerializer,
)

memberRepository = MemberRepositoryImpl()
memberService = MemberService(memberRepository)

teamRepository = TeamRepositoryImpl()
teamService = TeamService(teamRepository)


class MemberListView(APIView):
    http_method_names = ["get", "post"]

    def get(self, request: Request):
        members = to_dict_list(memberService.get_list())
        return Response(members)

    def post(self, request: Request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            member = memberService.create(
                data["name"], data["position"], data.get("team_id")
            )
            return Response(asdict(member))
        return Response(serializer.errors, status=400)


class MemberDetailView(APIView):
    http_method_names = ["get", "post", "delete"]

    def get(self, request: Request, pk: int):
        member = memberService.get_by_id(pk)
        if member is None:
            return Response(status=404)
        return Response(asdict(member))

    def post(self, request: Request, pk: int):
        request.data["id"] = pk
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            memberService.update(**serializer.validated_data)
            return Response()
        return Response(serializer.errors, status=400)

    def delete(self, request: Request, pk: int):
        serializer = MemberIdSerializer(data={"id": pk})
        if serializer.is_valid():
            memberService.remove(pk)
            return Response()
        return Response(serializer.errors, status=400)


class TeamListView(APIView):
    http_method_names = ["get", "post"]

    def get(self, request: Request):
        teams = to_dict_list(teamService.get_list())
        return Response(teams)

    def post(self, request: Request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            team = teamService.create(data["name"])
            return Response(asdict(team))
        return Response(serializer.errors, status=400)


class TeamDetailView(APIView):
    http_method_names = ["get", "post", "delete"]

    def get(self, request: Request, pk: int):
        team = teamService.get_by_id(pk)
        if team is None:
            return Response(status=404)
        return Response(asdict(team))

    def post(self, request: Request, pk: int):
        request.data["id"] = pk
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            teamService.update(**serializer.validated_data)
            return Response()
        return Response(serializer.errors, status=400)

    def delete(self, request: Request, pk: int):
        serializer = TeamIdSerializer(data={"id": pk})
        if serializer.is_valid():
            teamService.remove(pk)
            return Response()
        return Response(serializer.errors, status=400)
