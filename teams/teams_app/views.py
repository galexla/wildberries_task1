from dataclasses import asdict

from core.services import MemberService, TeamService, to_dict_list
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .repositories import MemberRepositoryImpl, TeamRepositoryImpl
from .serializers import (MemberIdSerializer, MemberSerializer,
                          TeamIdSerializer, TeamSerializer)

memberRepository = MemberRepositoryImpl()
memberService = MemberService(memberRepository)

teamRepository = TeamRepositoryImpl()
teamService = TeamService(teamRepository)


class MemberListView(APIView):
    http_method_names = ["get", "post"]

    @extend_schema(
        description="Retrieve a list of all members.",
        responses={status.HTTP_200_OK: MemberSerializer(many=True)},
    )
    def get(self, request: Request):
        members = to_dict_list(memberService.get_list())
        return Response(members)

    @extend_schema(
        description="Create a new member.",
        request=MemberSerializer,
        responses={
            status.HTTP_201_CREATED: MemberSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad Request"),
        }
    )
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

    @extend_schema(
        description="Retrieve details of a specific member by ID.",
        responses={
            status.HTTP_200_OK: MemberSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Not Found"),
        }
    )
    def get(self, request: Request, pk: int):
        member = memberService.get_by_id(pk)
        if member is None:
            return Response(status=404)
        return Response(asdict(member))

    @extend_schema(
        description="Update details of a specific member by ID.",
        request=MemberSerializer,
        responses={
            status.HTTP_200_OK: MemberSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad Request"),
        }
    )
    def post(self, request: Request, pk: int):
        request.data["id"] = pk
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            memberService.update(**serializer.validated_data)
            return Response()
        return Response(serializer.errors, status=400)

    @extend_schema(
        description="Delete a specific member by ID.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="No Content"),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad Request"),
        }
    )
    def delete(self, request: Request, pk: int):
        serializer = MemberIdSerializer(data={"id": pk})
        if serializer.is_valid():
            memberService.remove(pk)
            return Response()
        return Response(serializer.errors, status=400)


class TeamListView(APIView):
    http_method_names = ["get", "post"]

    @extend_schema(
        description="Retrieve a list of all teams.",
        responses={status.HTTP_200_OK: TeamSerializer(many=True)},
    )
    def get(self, request: Request):
        teams = to_dict_list(teamService.get_list())
        return Response(teams)

    @extend_schema(
        description="Create a new team.",
        request=TeamSerializer,
        responses={
            status.HTTP_201_CREATED: TeamSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad Request"),
        }
    )
    def post(self, request: Request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            team = teamService.create(data["name"])
            return Response(asdict(team))
        return Response(serializer.errors, status=400)


class TeamDetailView(APIView):
    http_method_names = ["get", "post", "delete"]

    @extend_schema(
        description="Retrieve details of a specific team by ID.",
        responses={
            status.HTTP_200_OK: TeamSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Not Found"),
        }
    )
    def get(self, request: Request, pk: int):
        team = teamService.get_by_id(pk)
        if team is None:
            return Response(status=404)
        return Response(asdict(team))

    @extend_schema(
        description="Update details of a specific team by ID.",
        request=TeamSerializer,
        responses={
            status.HTTP_200_OK: TeamSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad Request"),
        }
    )
    def post(self, request: Request, pk: int):
        request.data["id"] = pk
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            teamService.update(**serializer.validated_data)
            return Response()
        return Response(serializer.errors, status=400)

    @extend_schema(
        description="Delete a specific team by ID.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="No Content"),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad Request"),
        }
    )
    def delete(self, request: Request, pk: int):
        serializer = TeamIdSerializer(data={"id": pk})
        if serializer.is_valid():
            teamService.remove(pk)
            return Response()
        return Response(serializer.errors, status=400)
