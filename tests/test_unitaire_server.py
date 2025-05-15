from server import has_enough_points, has_enough_places_available, \
    update_booking, is_booking_limit_exceeded, get_list_ended_competitions, \
    is_competition_over


def test_has_enough_points_true():
    club = {'points': '10'}
    assert has_enough_points(club, 5) is True


def test_has_enough_points_false():
    club = {'points': '2'}
    assert has_enough_points(club, 3) is False


def test_has_enough_places_available():
    competition = {
        'numberOfPlaces': '10',
    }
    placesRequested = 5
    assert has_enough_places_available(competition, placesRequested) is True


def test_has_not_enough_places_available():
    competition = {
        'numberOfPlaces': '8',
    }
    placesRequested = 10
    assert has_enough_places_available(competition, placesRequested) is False


def test_update_booking_updates_points_and_places():
    club = {'name': 'Club X', 'points': '20'}
    competition = {'numberOfPlaces': '10', 'bookings': {'Club X': '2'}}
    update_booking(club, competition, 3)
    assert club['points'] == '17'
    assert competition['numberOfPlaces'] == '7'
    assert competition['bookings']['Club X'] == '5'


def test_update_booking_creates_booking_key_if_absent():
    club = {'name': 'Club X', 'points': '10'}
    competition = {'numberOfPlaces': '5'}
    update_booking(club, competition, 2)
    assert competition['bookings']['Club X'] == '2'


def test_is_booking_limit_exceeded_true():
    comp = {'bookings': {'Club X': '10'}}
    assert is_booking_limit_exceeded('Club X', comp, 3) is True


def test_is_booking_limit_exceeded_false():
    comp = {'bookings': {'Club X': '3'}}
    assert is_booking_limit_exceeded('Club X', comp, 5) is False


def test_is_booking_limit_exceeded_no_existing_booking():
    comp = {'bookings': {}}
    assert is_booking_limit_exceeded('Club X', comp, 10) is False


def test_get_list_Competitions_ended():
    past = {'name': 'Past', 'date': '2020-01-01 10:00:00'}
    future = {'name': 'Future',
              'date': '2099-01-01 10:00:00'}
    ended = get_list_ended_competitions([past, future])
    assert past in ended
    assert future not in ended


def test_is_competition_over_true():
    past_comp = {'name': 'Past Comp', 'date': '2022-01-01 10:00:00'}
    competitionsEnded = get_list_ended_competitions([past_comp])
    assert is_competition_over(past_comp, competitionsEnded) is True


def test_is_competition_over_false():
    future_comp = {'name': 'Future', 'date': '2099-01-01 10:00:00'}
    competitionsEnded = get_list_ended_competitions([future_comp])
    assert is_competition_over(future_comp, competitionsEnded) is False
