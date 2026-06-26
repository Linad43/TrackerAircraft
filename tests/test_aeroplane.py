import pytest

from src.model.aeroplane import Aeroplane


@pytest.fixture
def plane():
    return Aeroplane(
        "123abc",
        "SU123",
        "Russia",
        800.0,
        10000.0
    )


def test_to_dict(plane):
    assert plane.to_dict() == {
        "123abc": {
            "callsign": "SU123",
            "country": "Russia",
            "velocity": 800.0,
            "geo_altitude": 10000.0
        }
    }


def test_str(plane):
    assert str(plane) == "123abc: SU123, Russia, 800.0, 10000.0"


def test_repr(plane):
    assert repr(plane) == "[123abc] [SU123] [Russia] [800.0] [10000.0]"


def test_eq():
    plane1 = Aeroplane("1", "A", "Russia", 500, 1000)
    plane2 = Aeroplane("2", "B", "USA", 500, 1000)
    plane3 = Aeroplane("3", "C", "USA", 500, 2000)
    assert plane1 == plane2
    assert plane1 != plane3


def test_cast_to_object_list():
    data = {
        "time": 1766142246,
        "states": [
            [
                "4b1812",
                "SWR438A ",
                "Switzerland",
                1766166618,
                1766166618,
                -0.0168,
                51.0888,
                4267.2,
                False,
                189.7,
                129.39,
                14.63,
                None,
                4282.44,
                "2061",
                False,
                0
            ]
        ]
    }

    result = Aeroplane.cast_to_object_list(data)

    assert len(result) == 1
    assert result[0].icao24 == "4b1812"
    assert result[0].country == "Switzerland"
    assert result[0].velocity == 189.7
    assert result[0].geo_altitude == 4282.44
