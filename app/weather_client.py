import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

from app.models import WeatherReading

logger = logging.getLogger(__name__)

BASE_URL = "https://api.open-meteo.com/v1/forecast"
CURRENT_PARAMS = (
    "temperature_2m,apparent_temperature,precipitation,wind_speed_10m,weather_code"
)
MAX_RETRIES = 3

CITIES: dict[str, tuple[float, float]] = {
    "Ottawa": (45.42, -75.69),
    "Toronto": (43.70, -79.42),
    "Vancouver": (49.25, -123.12),
}


def _build_url(latitude: float, longitude: float) -> str:
    params = urllib.parse.urlencode(
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": CURRENT_PARAMS,
            "wind_speed_unit": "kmh",
            "timezone": "auto",
        }
    )
    return f"{BASE_URL}?{params}"


def _parse_response(city: str, data: dict) -> WeatherReading | None:
    current = data.get("current")
    if not isinstance(current, dict):
        return None

    required_fields = (
        "time",
        "weather_code",
        "temperature_2m",
        "apparent_temperature",
        "precipitation",
        "wind_speed_10m",
    )
    for field in required_fields:
        if field not in current or current[field] is None:
            return None

    return WeatherReading(
        city=city,
        timestamp=datetime.fromisoformat(current["time"]),
        weather_code=int(current["weather_code"]),
        temperature_2m=float(current["temperature_2m"]),
        apparent_temperature=float(current["apparent_temperature"]),
        precipitation=float(current["precipitation"]),
        wind_speed_10m=float(current["wind_speed_10m"]),
    )


def fetch_current_weather(city: str) -> WeatherReading | None:
    if city not in CITIES:
        raise ValueError(f"Unknown city: {city}")

    latitude, longitude = CITIES[city]
    url = _build_url(latitude, longitude)

    for attempt in range(1, MAX_RETRIES + 1):
        http_status: int | None = None
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                http_status = response.status
                payload = json.loads(response.read().decode())
            reading = _parse_response(city, payload)
            if reading is None:
                logger.warning(
                    "Invalid weather response for %s: missing required fields "
                    "(retry %s/%s)",
                    city,
                    attempt,
                    MAX_RETRIES,
                )
                continue
            return reading
        except urllib.error.HTTPError as exc:
            http_status = exc.code
            logger.warning(
                "Weather fetch failed for %s: %s HTTP %s (retry %s/%s)",
                city,
                type(exc).__name__,
                http_status,
                attempt,
                MAX_RETRIES,
            )
        except Exception as exc:
            logger.warning(
                "Weather fetch failed for %s: %s HTTP %s (retry %s/%s)",
                city,
                type(exc).__name__,
                http_status,
                attempt,
                MAX_RETRIES,
            )

    return None


def fetch_all_current_weather() -> list[WeatherReading]:
    readings: list[WeatherReading] = []
    for city in CITIES:
        reading = fetch_current_weather(city)
        if reading is not None:
            readings.append(reading)
    return readings
