import json

import pytest
from core.entities import Member, Team
from core.services import MemberService, TeamService
from django.urls import reverse
from rest_framework.test import APIClient
from teams_app.mappers import dataclass_from_dict
from teams_app.repositories import MemberRepositoryImpl, TeamRepositoryImpl

memberRepository = MemberRepositoryImpl()
memberService = MemberService(memberRepository)

teamRepository = TeamRepositoryImpl()
teamService = TeamService(teamRepository)


def json_text_to_dataclass(klass, json_text):
    d = json.loads(json_text)
    if isinstance(d, list):
        result = []
        for elem in d:
            result.append(dataclass_from_dict(klass, elem))
        return result
    else:
        return dataclass_from_dict(klass, d)


class TestMemberListView:
    @classmethod
    def setup_class(cls):
        cls.client = APIClient()

    @pytest.mark.django_db(transaction=True)
    def test_get(self, db_data):
        response = self.client.get(reverse("teams_app:members"))
        assert response.status_code == 200
        members = json_text_to_dataclass(Member, response.content)
        assert len(members) == 3
        assert members[0].id == "1"
        assert members[0].name == "Nick"
        assert members[0].team_id == "1"
        assert members[1].position == "backend developer"
        assert members[1].team_id == "1"
        assert members[2].name == "Jack"
        assert members[2].team_id is None

    @pytest.mark.django_db(transaction=True)
    def test_post(self, db_data):
        response = self.client.post(
            reverse("teams_app:members"),
            {"name": "Jack", "position": "position1"},
        )
        assert response.status_code == 200
        member = json_text_to_dataclass(Member, response.content)
        assert member.name == "Jack"
        assert member.position == "position1"

        response = self.client.post(
            reverse("teams_app:members"),
            {"name": "Test", "position": "position2", "team_id": 1},
        )
        assert response.status_code == 200
        member = json_text_to_dataclass(Member, response.content)
        assert member.name == "Test"
        assert member.position == "position2"
        assert member.team_id == "1"

        response = self.client.post(
            reverse("teams_app:members"),
            {"name": "Jack"},
        )
        assert response.status_code == 400

        response = self.client.post(reverse("teams_app:members"), {})
        assert response.status_code == 400

        response = self.client.post(
            reverse("teams_app:members"),
            {"name": "Test", "position": "position2", "team_id": 2},
        )
        assert response.status_code == 400


class TestMemberDetailView:
    @classmethod
    def setup_class(cls):
        cls.client = APIClient()

    @pytest.mark.django_db(transaction=True)
    def test_get(self, db_data):
        response = self.client.get(
            reverse("teams_app:member", kwargs={"pk": 1})
        )
        assert response.status_code == 200
        member = json_text_to_dataclass(Member, response.content)
        assert member.name == "Nick"
        assert member.position == "frontend developer"

        response = self.client.get(
            reverse("teams_app:member", kwargs={"pk": 100})
        )
        assert response.status_code == 404

        response = self.client.get(
            reverse("teams_app:member", kwargs={"pk": 0})
        )
        assert response.status_code == 404

    @pytest.mark.django_db(transaction=True)
    def test_post(self, db_data):
        response = self.client.post(
            reverse("teams_app:member", kwargs={"pk": 1}),
            {"name": "Jack", "position": "position1"},
        )
        assert response.status_code == 200
        member = memberService.get_by_id(1)
        assert member.name == "Jack"
        assert member.position == "position1"

        response = self.client.post(
            reverse("teams_app:member", kwargs={"pk": 1}),
            {"position": "position2"},
        )
        assert response.status_code == 400

        response = self.client.post(
            reverse("teams_app:member", kwargs={"pk": 1}), {}
        )
        assert response.status_code == 400

        response = self.client.post(
            reverse("teams_app:member", kwargs={"pk": 3}),
            {"name": "Jack", "position": "backend developer", "team_id": 1},
        )
        assert response.status_code == 200
        member = memberService.get_by_id(3)
        assert member.name == "Jack"
        assert member.position == "backend developer"
        assert member.team_id == "1"

        response = self.client.post(
            reverse("teams_app:member", kwargs={"pk": 3}),
            {"name": "Jack", "position": "backend developer", "team_id": 2},
        )
        assert response.status_code == 400

        response = self.client.post(
            reverse("teams_app:member", kwargs={"pk": 100}),
            {"name": "Jack", "position": "backend developer", "team_id": 1},
        )
        assert response.status_code == 400

        response = self.client.post(
            reverse("teams_app:member", kwargs={"pk": 0}),
            {"name": "Jack", "position": "backend developer", "team_id": 1},
        )
        assert response.status_code == 400

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, db_data):
        response = self.client.delete(
            reverse("teams_app:member", kwargs={"pk": 1})
        )
        assert response.status_code == 200
        assert memberService.get_by_id(1) is None

        response = self.client.delete(
            reverse("teams_app:member", kwargs={"pk": 0})
        )
        assert response.status_code == 400

        response = self.client.delete(
            reverse("teams_app:member", kwargs={"pk": 100})
        )
        assert response.status_code == 400


class TestTeamListView:
    @classmethod
    def setup_class(cls):
        cls.client = APIClient()

    @pytest.mark.django_db(transaction=True)
    def test_get(self, db_data):
        response = self.client.get(reverse("teams_app:teams"))
        assert response.status_code == 200
        teams = json_text_to_dataclass(Team, response.content)
        assert len(teams) == 1
        assert teams[0].id == 1
        assert teams[0].name == "Team1"
        assert set(teams[0].members) == set(["1", "2"])

    @pytest.mark.django_db(transaction=True)
    def test_post(self, db_data):
        response = self.client.post(
            reverse("teams_app:teams"),
            {"name": "Team2"},
        )
        assert response.status_code == 200
        team = json_text_to_dataclass(Team, response.content)
        assert team.name == "Team2"

        response = self.client.post(
            reverse("teams_app:teams"), {"test": "Test"}
        )
        assert response.status_code == 400

        response = self.client.post(reverse("teams_app:teams"), {})
        assert response.status_code == 400


class TestTeamDetailView:
    @classmethod
    def setup_class(cls):
        cls.client = APIClient()

    @pytest.mark.django_db(transaction=True)
    def test_get(self, db_data):
        response = self.client.get(reverse("teams_app:team", kwargs={"pk": 1}))
        assert response.status_code == 200
        team = json_text_to_dataclass(Team, response.content)
        assert team.name == "Team1"

        response = self.client.get(
            reverse("teams_app:team", kwargs={"pk": 100})
        )
        assert response.status_code == 404

        response = self.client.get(reverse("teams_app:team", kwargs={"pk": 0}))
        assert response.status_code == 404

    @pytest.mark.django_db(transaction=True)
    def test_post(self, db_data):
        response = self.client.post(
            reverse("teams_app:team", kwargs={"pk": 1}), {"name": "Team2"}
        )
        assert response.status_code == 200
        team = teamService.get_by_id(1)
        assert team.name == "Team2"

        response = self.client.post(
            reverse("teams_app:team", kwargs={"pk": 1}), {"test": "test"}
        )
        assert response.status_code == 400

        response = self.client.post(
            reverse("teams_app:team", kwargs={"pk": 100}), {"name": "Team2"}
        )
        assert response.status_code == 400

        response = self.client.post(
            reverse("teams_app:team", kwargs={"pk": 0}), {"name": "Team2"}
        )
        assert response.status_code == 400

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, db_data):
        response = self.client.delete(
            reverse("teams_app:team", kwargs={"pk": 1})
        )
        assert response.status_code == 200
        assert teamService.get_by_id(1) is None

        response = self.client.delete(
            reverse("teams_app:team", kwargs={"pk": 0})
        )
        assert response.status_code == 400

        response = self.client.delete(
            reverse("teams_app:team", kwargs={"pk": 100})
        )
        assert response.status_code == 400
