import pytest
from server import app, loadClubs, loadCompetitions, saveClubs, \
    saveCompetitions, clubs, competitions


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


def test_save_clubs_calls_json_dump(mocker):
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)
    mock_dump = mocker.patch("json.dump")

    saveClubs([{"name": "X", "points": "1"}])

    mock_dump.assert_called_once()


def test_save_competitions_calls_json_dump(mocker):
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)
    mock_dump = mocker.patch("json.dump")

    saveCompetitions([{"name": "X", "points": "1"}])

    mock_dump.assert_called_once()


def test_booking_calls_saves(mocker, client):
    club = clubs[0]
    competition = competitions[1]

    mock_save_clubs = mocker.patch("server.saveClubs")
    mock_save_comps = mocker.patch("server.saveCompetitions")

    client.post('/login', data={'email': club['email']}, follow_redirects=True)
    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': '1'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    mock_save_clubs.assert_called_once()
    mock_save_comps.assert_called_once()

