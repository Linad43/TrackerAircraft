from unittest.mock import Mock, patch

from src.services.apiAdapter import APIAdapter


@patch("src.services.apiAdapter.get")
def test_get_aeroplanes(mock_get):
    response1 = Mock()
    response1.json.return_value = [
        {
            "boundingbox": ["1", "2", "3", "4"]
        }
    ]

    response2 = Mock()
    response2.json.return_value = {
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

    mock_get.side_effect = [response1, response2]
    adapter = APIAdapter()
    result = adapter.get_aeroplanes("Russia")
    assert result == {
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
    assert adapter.geo_coordinates == ["1", "2", "3", "4"]
