from datetime import datetime, timedelta

import pandas as pd
from dagster import (
    AssetCheckResult,
    Definitions,
    ScheduleDefinition,
    asset,
    asset_check,
    define_asset_job,
)

import db
import source


def _build_weather_dataframe(payload: dict) -> pd.DataFrame:
    """Convert Open-Meteo API response into a structured DataFrame."""
    daily = payload["daily"]
    return pd.DataFrame(
        {
            "date": daily["time"],
            "temp_max_c": daily["temperature_2m_max"],
            "temp_min_c": daily["temperature_2m_min"],
            "precipitation_mm": daily["precipitation_sum"],
            "wind_speed_max_kmh": daily["wind_speed_10m_max"],
        }
    )


@asset
def raw_weather_data() -> pd.DataFrame:
    """Fetch daily weather data for Jakarta from Open-Meteo API.

    Fetches the last 7 days of weather data by default.
    """
    today = datetime.now()
    end_date = today.strftime("%Y-%m-%d")
    start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")

    payload = source.fetch_weather(
        latitude=source.DEFAULT_LATITUDE,
        longitude=source.DEFAULT_LONGITUDE,
        start_date=start_date,
        end_date=end_date,
    )
    return _build_weather_dataframe(payload)


@asset
def weather_table(raw_weather_data: pd.DataFrame) -> int:
    """Load weather data into the warehouse Postgres `weather` table."""
    return db.load_table(raw_weather_data, "weather")


@asset_check(asset=raw_weather_data)
def weather_data_not_empty(raw_weather_data: pd.DataFrame) -> AssetCheckResult:
    """Ensure weather data was fetched successfully and is not empty."""
    return AssetCheckResult(
        passed=not raw_weather_data.empty,
        metadata={
            "row_count": len(raw_weather_data),
            "date_range": f"{raw_weather_data['date'].min()} to {raw_weather_data['date'].max()}"
            if not raw_weather_data.empty
            else "N/A",
        },
    )


refresh_weather_job = define_asset_job(name="refresh_weather_job")

refresh_weather_daily = ScheduleDefinition(
    name="refresh_weather_daily",
    job=refresh_weather_job,
    cron_schedule="0 7 * * *",
)

defs = Definitions(
    assets=[
        raw_weather_data,
        weather_table,
    ],
    asset_checks=[
        weather_data_not_empty,
    ],
    jobs=[
        refresh_weather_job,
    ],
    schedules=[
        refresh_weather_daily,
    ],
)

