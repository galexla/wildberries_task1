import pytest
from teams_app.repositories import MemberRepositoryImpl, TeamRepositoryImpl


class TestMemberRepositoryImpl:
    @pytest.mark.django_db(transaction=True)
    def test_create(self, db_data):
        repo = MemberRepositoryImpl()
        member = repo.create("Jack", "position1")
        assert member.name == "Jack"
        assert member.position == "position1"

    @pytest.mark.django_db(transaction=True)
    def test_get_by_id(self, db_data):
        repo = MemberRepositoryImpl()
        member = repo.get_by_id(1)
        assert member.name == "Nick"
        assert member.position == "frontend developer"

    @pytest.mark.django_db(transaction=True)
    def test_remove(self, db_data):
        repo = MemberRepositoryImpl()
        member = repo.remove(1)
        member = repo.get_by_id(1)
        assert member is None


class TestTeamRepositoryImpl:
    @pytest.mark.django_db(transaction=True)
    def test_create(self, db_data):
        repo = TeamRepositoryImpl()
        team = repo.create("Team2")
        assert team.name == "Team2"

    @pytest.mark.django_db(transaction=True)
    def test_get_by_id(self, db_data):
        repo = TeamRepositoryImpl()
        team = repo.get_by_id(1)
        assert team.name == "Team1"
        assert set(team.members) == set(["1", "2"])

    @pytest.mark.django_db(transaction=True)
    def test_add_member(self, db_data):
        repo = TeamRepositoryImpl()
        repo.add_member(1, 3)
        team = repo.get_by_id(1)
        assert set(team.members) == set(["1", "2", "3"])

    @pytest.mark.django_db(transaction=True)
    def test_add_members(self, db_data):
        repo = TeamRepositoryImpl()
        team = repo.create("Team2")
        repo.add_members(team.id, [1, 3])
        team = repo.get_by_id(team.id)
        assert set(team.members) == set(["1", "3"])

    @pytest.mark.django_db(transaction=True)
    def test_remove_member(self, db_data):
        repo = TeamRepositoryImpl()
        repo.remove_member(1, 2)
        team = repo.get_by_id(1)
        assert set(team.members) == set(["1"])

    @pytest.mark.django_db(transaction=True)
    def test_remove_members(self, db_data):
        repo = TeamRepositoryImpl()
        repo.remove_members(1, [1, 2])
        team = repo.get_by_id(1)
        assert len(team.members) == 0

    @pytest.mark.django_db(transaction=True)
    def test_remove(self, db_data):
        repo = TeamRepositoryImpl()
        team = repo.get_by_id(1)
        assert team is not None
        team = repo.remove(1)
        team = repo.get_by_id(1)
        assert team is None
