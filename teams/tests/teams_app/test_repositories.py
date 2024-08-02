import pytest
from teams_app.repositories import MemberRepositoryImpl, TeamRepositoryImpl


class TestMemberRepositoryImpl:
    @pytest.mark.django_db(transaction=True)
    def test_get_list(self, db_data):
        repo = MemberRepositoryImpl()
        members = repo.get_list()
        assert len(members) == 3
        assert members[0].id == "1"
        assert members[0].name == "Nick"
        assert members[0].team_id == "1"
        assert members[1].position == "backend developer"
        assert members[1].team_id == "1"
        assert members[2].name == "Jack"
        assert members[2].team_id is None

    @pytest.mark.django_db(transaction=True)
    def test_create(self, db_data):
        repo = MemberRepositoryImpl()
        member = repo.create("Jack", "position1")
        assert member.name == "Jack"
        assert member.position == "position1"

    @pytest.mark.django_db(transaction=True)
    def test_update(self, db_data):
        repo = MemberRepositoryImpl()
        repo.update(1, name="Jack", position="position1")
        member = repo.get_by_id(1)
        assert member.name == "Jack"
        assert member.position == "position1"

    @pytest.mark.django_db(transaction=True)
    def test_get_by_id(self, db_data):
        repo = MemberRepositoryImpl()
        member = repo.get_by_id(1)
        assert member.name == "Nick"
        assert member.position == "frontend developer"

    @pytest.mark.django_db(transaction=True)
    def test_set_team_id(self, db_data):
        repo = MemberRepositoryImpl()
        member = repo.set_team_id(3, 1)
        member = repo.get_by_id(3)
        assert member.team_id == "1"

    @pytest.mark.django_db(transaction=True)
    def test_remove(self, db_data):
        repo = MemberRepositoryImpl()
        member = repo.remove(1)
        member = repo.get_by_id(1)
        assert member is None


class TestTeamRepositoryImpl:
    @pytest.mark.django_db(transaction=True)
    def test_get_list(self, db_data):
        repo = TeamRepositoryImpl()
        teams = repo.get_list()
        assert len(teams) == 1
        assert teams[0].id == 1
        assert teams[0].name == "Team1"
        assert set(teams[0].members) == set(["1", "2"])

    @pytest.mark.django_db(transaction=True)
    def test_create(self, db_data):
        repo = TeamRepositoryImpl()
        team = repo.create("Team2")
        assert team.name == "Team2"

    @pytest.mark.django_db(transaction=True)
    def test_update(self, db_data):
        repo = TeamRepositoryImpl()
        repo.update(1, name="Team3")
        team = repo.get_by_id(1)
        assert team.name == "Team3"

    @pytest.mark.django_db(transaction=True)
    def test_get_by_id(self, db_data):
        repo = TeamRepositoryImpl()
        team = repo.get_by_id(1)
        assert team.name == "Team1"
        assert set(team.members) == set(["1", "2"])

    @pytest.mark.django_db(transaction=True)
    def test_remove(self, db_data):
        repo = TeamRepositoryImpl()
        team = repo.get_by_id(1)
        assert team is not None
        team = repo.remove(1)
        team = repo.get_by_id(1)
        assert team is None
