import pytest
from server import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_load_clubs_reads_json_file(mocker):
    mock_open = mocker.mock_open(read_data='{"clubs": ['
                                           '{"name": "Test Club", '
                                           '"email": "test@test.com", '
                                           '"points": "10"}]}')
    mocker.patch("builtins.open", mock_open)

    result = loadClubs()
    assert result[0]["name"] == "Test Club"


def test_load_competitions_reads_json_file(mocker):
    mock_open = mocker.mock_open(
        read_data='{"competitions": [ '
                  '{"name": "Fake Competition", '
                  '"date": "2099-12-31 10:00:00", '
                  '"numberOfPlaces": "5", '
                  '"bookings": {} }]}')
    mocker.patch("builtins.open", mock_open)

    result = loadCompetitions()
    assert result[0]["name"] == "Fake Competition"
