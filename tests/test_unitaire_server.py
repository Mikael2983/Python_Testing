import pytest
from server import has_enough_points, has_enough_places_available


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
