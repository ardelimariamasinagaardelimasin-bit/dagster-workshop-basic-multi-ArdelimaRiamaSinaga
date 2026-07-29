from unittest.mock import Mock, patch

import pytest
import requests

import source


def test_fetch_weather_returns_parsed_json():
    fake_response = Mock()
    fake_response.json.return_value = {
        "latitude": -6.21,
        "longitude": 106.85,
        "daily": {
            "time": ["2025-01-01", "2025-01-02"],
            "temperature_2m_max": [30.5, 31.2],
            "temperature_2m_min": [24.1, 24.5],
            "precipitation_sum": [0.0, 5.2],
            "wind_speed_10m_max": [12.3, 15.8],
        },
    }
    fake_response.raise_for_status.return_value = None

    with patch("source.requests.get", return_value=fake_response) as mock_get:
        result = source.fetch_weather(
            latitude=-6.2088,
            longitude=106.8456,
            start_date="2025-01-01",
            end_date="2025-01-02",
        )

    assert result["daily"]["time"] == ["2025-01-01", "2025-01-02"]
    assert result["daily"]["temperature_2m_max"] == [30.5, 31.2]
    mock_get.assert_called_once_with(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": -6.2088,
            "longitude": 106.8456,
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "timezone": "Asia/Jakarta",
        },
        timeout=30,
    )


def test_fetch_weather_raises_source_unavailable_on_network_error():
    with patch("source.requests.get", side_effect=requests.ConnectionError("boom")):
        with pytest.raises(source.SourceUnavailableError):
            source.fetch_weather()

