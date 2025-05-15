import pytest

from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def fake_data():
    fake_club = [{
        'name': 'Fake_Club',
        'email': 'fake@club.com',
        'points': '10'
    }]
    fake_competition = [
        {
            'name': 'Old_Comp',
            'date': '2020-01-01 10:00:00',
            'numberOfPlaces': '5',
            'bookings': {}
        },
        {
            'name': 'Fake_Competition',
            'date': '2099-12-31 10:00:00',
            'numberOfPlaces': '5',
            'bookings': {}
        }]
    return fake_club, fake_competition


def test_login_valid_email(client, mocker, fake_data):
    clubs, competitions = fake_data
    mocker.patch("server.clubs", clubs)
    mocker.patch("server.competitions", competitions)

    response = client.post('/login', data={'email': 'fake@club.com'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome, fake@club.com" in response.data


def test_login_invalid_email(client, mocker, fake_data):
    clubs, _ = fake_data
    mocker.patch("server.clubs", clubs)

    response = client.post('/login', data={'email': 'wrong@mail.com'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b"Sorry, that email wasn&#39;t found" in response.data


def test_show_summary_requires_login(client):
    response = client.get('/showSummary', follow_redirects=True)
    assert b"You must be logged in" in response.data


def test_show_summary_renders_welcome(client, mocker, fake_data):
    clubs, competitions = fake_data
    club = clubs[0]

    mocker.patch("server.clubs", clubs)
    mocker.patch("server.competitions", competitions)

    client.post("/login", data={"email": club["email"]}, follow_redirects=True)

    response = client.get("/showSummary", follow_redirects=True)

    assert response.status_code == 200
    assert b"Competitions:" in response.data


def test_book_requires_login(client, fake_data):
    clubs, competitions = fake_data
    competition_name = competitions[1]['name']
    club_name = clubs[0]['name']
    response = client.get(f'/book/{competition_name}/{club_name}',
                          follow_redirects=True)
    assert b"You must be logged in" in response.data


def test_purchasePlaces_requires_login(client):

    data = {
        'competition': 'Spring Festival',
        'club': "Simply Lift",
        'places': '1'}
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)

    assert b"You must be logged in" in response.data


def test_logout_requires_login(client):

    response = client.get(f'/logout',
                          follow_redirects=True)

    assert b"You must be logged in" in response.data


def test_logout_clears_session_and_redirects(client, mocker, fake_data):
    clubs, _ = fake_data
    club = clubs[0]

    mocker.patch("server.clubs", clubs)

    client.post("/login", data={"email": club["email"]}, follow_redirects=True)

    with client.session_transaction() as session:
        assert 'club' in session

    response = client.get("/logout", follow_redirects=True)

    with client.session_transaction() as session:
        assert 'club' not in session

    assert response.status_code == 200
    assert b"secretary email" in response.data