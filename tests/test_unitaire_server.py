import pytest
from server import has_enough_points


def test_has_enough_points_true():
    club = {'points': '10'}
    assert has_enough_points(club, 5) is True


def test_has_enough_points_false():
    club = {'points': '2'}
    assert has_enough_points(club, 3) is False
