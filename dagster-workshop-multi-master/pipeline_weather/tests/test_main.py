from unittest.mock import patch

import pandas as pd
from dagster import materialize

import db
import source
from main import raw_weather_data, weather_table

FAKE_PAYLOAD = {
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


def test_weather_pipeline_loads_expected_rows():
    loaded = {}

    def fake_load_table(df: pd.DataFrame, table_name: str) -> int:
        loaded[table_name] = df
        return len(df)

    with patch.object(source, "fetch_weather", return_value=FAKE_PAYLOAD), patch.object(
        db, "load_table", side_effect=fake_load_table
    ):
        result = materialize([raw_weather_data, weather_table])

    assert result.success
    assert loaded["weather"].shape[0] == 2
    assert loaded["weather"].loc[0, "temp_max_c"] == 30.5
    assert loaded["weather"].loc[1, "precipitation_mm"] == 5.2
    assert list(loaded["weather"].columns) == [
        "date",
        "temp_max_c",
        "temp_min_c",
        "precipitation_mm",
        "wind_speed_max_kmh",
    ]

