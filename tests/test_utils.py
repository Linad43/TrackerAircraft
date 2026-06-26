import pytest

from src.model.aeroplane import Aeroplane
from src.services import utils


@pytest.fixture
def aeroplanes():
    return [
        Aeroplane("1", "SU001", "Russia", 800, 10000),
        Aeroplane("2", "AA001", "USA", 850, 12000),
        Aeroplane("3", "LH001", "Germany", 700, 8000),
        Aeroplane("4", "AF001", "France", 900, None),
        Aeroplane("5", "UN001", None, 600, 15000),
    ]


def test_filter_aeroplanes(aeroplanes):
    result = utils.filter_aeroplanes(aeroplanes, ["russia", "usa"])
    assert len(result) == 2
    assert result[0].country == "Russia"
    assert result[1].country == "USA"


def test_filter_aeroplanes_case_insensitive(aeroplanes):
    result = utils.filter_aeroplanes(aeroplanes, ["RuSsIa"])
    assert len(result) == 1
    assert result[0].country == "Russia"


def test_get_aeroplanes_by_altitude(aeroplanes):
    result = utils.get_aeroplanes_by_altitude(aeroplanes, "9000 - 13000")
    assert len(result) == 2


def test_sort_aeroplanes(aeroplanes):
    result = utils.sort_aeroplanes(aeroplanes[:3])
    assert [plane.country for plane in result] == [
        "Germany",
        "Russia",
        "USA",
    ]


def test_get_top_aeroplanes(aeroplanes):
    result = utils.get_top_aeroplanes(aeroplanes, 2)
    assert result == aeroplanes[:2]


def test_get_top_aeroplanes_more_than_length(aeroplanes):
    result = utils.get_top_aeroplanes(aeroplanes, 10)
    assert result == aeroplanes
