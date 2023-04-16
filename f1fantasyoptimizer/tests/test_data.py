import pytest
import f1fantasyoptimizer.data as data
import f1fantasyoptimizer.tests.utils as utils


def test_create_team_from_names_success():
    pick_data = utils.get_pick_data()
    team_names = utils.get_team_names()
    team = data.create_team_from_names(team_names, pick_data)
    assert team
    assert team[0].name == team_names[0][0]
    assert team[1].name == team_names[0][1]
    assert team[2].name == team_names[0][2]
    assert team[3].name == team_names[0][3]
    assert team[4].name == team_names[0][4]
    assert team[5].name == team_names[0][5]
    assert team[6].name == team_names[0][6]
    assert team[0].td is True
    assert team[1].td is False
    assert team[2].td is False
    assert team[3].td is False
    assert team[4].td is False
    assert team[5].td is False
    assert team[6].td is False


def test_create_team_from_names_invalid_td():
    pick_data = utils.get_pick_data()
    team_names = utils.get_team_names()
    invalid_td_team_names = (team_names[0], team_names[0][5])  # turbo driver can't be a constructor
    with pytest.raises(ValueError):
        data.create_team_from_names(invalid_td_team_names, pick_data)


def test_find_pick_by_name():
    pick_data = utils.get_pick_data()
    assert data.find_pick_by_name(pick_data, name="Max Verstappen") == 131


def test_to_float():
    assert data.to_float("131.1", default=3.3) == 131.1
    assert data.to_float("", default=3.3) == 3.3
    assert data.to_float("") == 0.0
