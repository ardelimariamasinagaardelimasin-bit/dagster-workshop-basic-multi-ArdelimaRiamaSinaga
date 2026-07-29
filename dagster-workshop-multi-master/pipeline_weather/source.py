import requests

# Open-Meteo API (free, no API key required)
BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

# Default location: Jakarta, Indonesia
DEFAULT_LATITUDE = -6.2088
DEFAULT_LONGITUDE = 106.8456

# Daily weather parameters to fetch
DAILY_PARAMS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
]


class SourceUnavailableError(Exception):
    """Raised when the Open-Meteo API cannot be reached."""


def fetch_weather(
    latitude: float = DEFAULT_LATITUDE,
    longitude: float = DEFAULT_LONGITUDE,
    start_date: str = "2025-01-01",
    end_date: str = "2025-12-31",
) -> dict:
    """Fetch historical daily weather data from Open-Meteo API.

    Parameters
    ----------
    latitude : float
        Latitude of the location (default: Jakarta).
    longitude : float
        Longitude of the location (default: Jakarta).
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.

    Returns
    -------
    dict
        Parsed JSON response with daily weather data.

    Raises
    ------
    SourceUnavailableError
        If the API cannot be reached.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(DAILY_PARAMS),
        "timezone": "Asia/Jakarta",
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise SourceUnavailableError(
            "Could not reach Open-Meteo API — check your internet connection"
        ) from exc
    return response.json()

