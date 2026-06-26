import json

from src.model.aeroplane import Aeroplane
from src.model.jsonSaver import JSONSaver


def test_add_aeroplane(tmp_path):
    saver = JSONSaver("test.json")
    saver.file_name = tmp_path / "test.json"
    saver.file_name.write_text("{}", encoding="utf-8")
    plane = Aeroplane(
        "abc",
        "SU123",
        "Russia",
        800,
        10000
    )
    saver.add_aeroplane(plane)
    data = json.loads(saver.file_name.read_text(encoding="utf-8"))
    assert "abc" in data


def test_delete_aeroplane(tmp_path):
    saver = JSONSaver("test.json")
    saver.file_name = tmp_path / "test.json"
    saver.file_name.write_text(
        json.dumps({
            "abc": {
                "callsign": "SU123",
                "country": "Russia",
                "velocity": 800,
                "geo_altitude": 10000
            }
        }),
        encoding="utf-8"
    )
    plane = Aeroplane(
        "abc",
        "",
        "",
        0,
        0
    )
    assert saver.delete_aeroplane(plane)


def test_load(tmp_path):
    saver = JSONSaver("test.json")
    saver.file_name = tmp_path / "test.json"

    data = {
        "abc": {
            "callsign": "SU123",
            "country": "Russia",
            "velocity": 800,
            "geo_altitude": 10000
        },
        "def": {
            "callsign": "AA456",
            "country": "USA",
            "velocity": 900,
            "geo_altitude": 11000
        }
    }

    saver.file_name.write_text(
        json.dumps(data),
        encoding="utf-8"
    )

    result = saver.load()

    assert len(result) == 2

    assert result[0].icao24 == "abc"
    assert result[0].callsign == "SU123"
    assert result[0].country == "Russia"

    assert result[1].icao24 == "def"
    assert result[1].callsign == "AA456"
    assert result[1].country == "USA"
