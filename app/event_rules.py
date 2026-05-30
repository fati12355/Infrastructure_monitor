from datetime import datetime, timezone
from typing import Any

from app.models import NotableEvent, WeatherReading


def _make_event(
    *,
    city: str,
    rule_name: str,
    alert_level: str,
    message: str,
    reading: WeatherReading,
    triggered_values: dict[str, Any],
    event_timestamp: datetime | None = None,
) -> NotableEvent:
    return NotableEvent(
        city=city,
        timestamp=event_timestamp or datetime.now(timezone.utc),
        rule_name=rule_name,
        alert_level=alert_level,
        message=message,
        reading_timestamp=reading.timestamp,
        triggered_values=triggered_values,
    )


def _newly_triggered(current_met: bool, previous_met: bool) -> bool:
    return current_met and not previous_met


def vancouver_late_spring_squall(
    current: WeatherReading,
    previous: WeatherReading | None,
) -> NotableEvent | None:
    if previous is None or current.city != "Vancouver":
        return None

    current_met = current.weather_code in (81, 82) and current.wind_speed_10m >= 45.0
    previous_met = previous.weather_code in (81, 82) and previous.wind_speed_10m >= 45.0
    if not _newly_triggered(current_met, previous_met):
        return None

    return _make_event(
        city="Vancouver",
        rule_name="vancouver_late_spring_squall",
        alert_level="Yellow Advisory",
        message=(
            "Heavy rain showers and strong winds are hitting Vancouver. "
            "Stay off the water and use caution on coastal routes."
        ),
        reading=current,
        triggered_values={
            "weather_code": current.weather_code,
            "wind_speed_10m": current.wind_speed_10m,
        },
    )


def toronto_early_heatwave_shock(
    current: WeatherReading,
    previous: WeatherReading | None,
) -> NotableEvent | None:
    if previous is None or current.city != "Toronto":
        return None

    current_met = (
        current.apparent_temperature >= 35.0 and current.temperature_2m >= 30.0
    )
    previous_met = (
        previous.apparent_temperature >= 35.0 and previous.temperature_2m >= 30.0
    )
    if not _newly_triggered(current_met, previous_met):
        return None

    return _make_event(
        city="Toronto",
        rule_name="toronto_early_heatwave_shock",
        alert_level="Orange Warning",
        message=(
            "Humidex is 35°C or higher in Toronto. Limit outdoor activity, "
            "stay hydrated, and check on vulnerable neighbours."
        ),
        reading=current,
        triggered_values={
            "apparent_temperature": current.apparent_temperature,
            "temperature_2m": current.temperature_2m,
        },
    )


def ottawa_flash_urban_flood(
    current: WeatherReading,
    previous: WeatherReading | None,
) -> NotableEvent | None:
    if previous is None or current.city != "Ottawa":
        return None

    current_met = (
        current.weather_code in (65, 82) and current.precipitation >= 25.0
    )
    previous_met = (
        previous.weather_code in (65, 82) and previous.precipitation >= 25.0
    )
    if not _newly_triggered(current_met, previous_met):
        return None

    return _make_event(
        city="Ottawa",
        rule_name="ottawa_flash_urban_flood",
        alert_level="Orange Warning",
        message=(
            "Heavy rain is falling in Ottawa with high accumulation. "
            "Avoid flooded roads and watch for basement flooding."
        ),
        reading=current,
        triggered_values={
            "weather_code": current.weather_code,
            "precipitation": current.precipitation,
        },
    )


def severe_microburst_thunderstorm_wind(
    current: WeatherReading,
    previous: WeatherReading | None,
) -> NotableEvent | None:
    if previous is None:
        return None

    current_met = (
        current.weather_code in (95, 96, 99) and current.wind_speed_10m >= 60.0
    )
    previous_met = (
        previous.weather_code in (95, 96, 99) and previous.wind_speed_10m >= 60.0
    )
    if not _newly_triggered(current_met, previous_met):
        return None

    return _make_event(
        city=current.city,
        rule_name="severe_microburst_thunderstorm_wind",
        alert_level="Orange Warning",
        message=(
            f"Thunderstorm winds are dangerously strong in {current.city}. "
            "Stay indoors, away from windows, and watch for downed trees or power lines."
        ),
        reading=current,
        triggered_values={
            "weather_code": current.weather_code,
            "wind_speed_10m": current.wind_speed_10m,
        },
    )


def toronto_commuter_flash_freeze(
    current: WeatherReading,
    previous: WeatherReading | None,
) -> NotableEvent | None:
    if previous is None or current.city != "Toronto":
        return None

    current_met = (
        current.weather_code in (96, 99) and current.precipitation >= 15.0
    )
    previous_met = (
        previous.weather_code in (96, 99) and previous.precipitation >= 15.0
    )
    if not _newly_triggered(current_met, previous_met):
        return None

    return _make_event(
        city="Toronto",
        rule_name="toronto_commuter_flash_freeze",
        alert_level="Orange Warning",
        message=(
            "Hail and heavy rain are hitting Toronto highways. "
            "Slow down, increase following distance, and delay non-essential travel."
        ),
        reading=current,
        triggered_values={
            "weather_code": current.weather_code,
            "precipitation": current.precipitation,
        },
    )


def vancouver_coastal_fog_blindspot(
    current: WeatherReading,
    previous: WeatherReading | None,
) -> NotableEvent | None:
    if previous is None or current.city != "Vancouver":
        return None

    current_met = (
        current.weather_code in (45, 48) and current.wind_speed_10m <= 10.0
    )
    previous_met = (
        previous.weather_code in (45, 48) and previous.wind_speed_10m <= 10.0
    )
    if not _newly_triggered(current_met, previous_met):
        return None

    return _make_event(
        city="Vancouver",
        rule_name="vancouver_coastal_fog_blindspot",
        alert_level="Yellow Advisory",
        message=(
            "Dense fog with little wind in Vancouver. "
            "Allow extra travel time and use extra caution on roads and on the water."
        ),
        reading=current,
        triggered_values={
            "weather_code": current.weather_code,
            "wind_speed_10m": current.wind_speed_10m,
        },
    )


def ottawa_stagnant_smog_trap(
    current: WeatherReading,
    previous: WeatherReading | None,
) -> NotableEvent | None:
    if previous is None or current.city != "Ottawa":
        return None

    current_met = (
        current.temperature_2m >= 28.0 and current.wind_speed_10m <= 8.0
    )
    previous_met = (
        previous.temperature_2m >= 28.0 and previous.wind_speed_10m <= 8.0
    )
    if not _newly_triggered(current_met, previous_met):
        return None

    return _make_event(
        city="Ottawa",
        rule_name="ottawa_stagnant_smog_trap",
        alert_level="Yellow Advisory",
        message=(
            "Heat built up in Ottawa without wind to disperse it. "
            "Exercise caution if you have breathing sensitivity."
        ),
        reading=current,
        triggered_values={
            "temperature_2m": current.temperature_2m,
            "wind_speed_10m": current.wind_speed_10m,
        },
    )


def instability_transfer_toronto_to_ottawa(
    toronto: WeatherReading,
    toronto_previous: WeatherReading | None,
    ottawa: WeatherReading,
    ottawa_previous: WeatherReading | None,
) -> NotableEvent | None:
    if toronto_previous is None or ottawa_previous is None:
        return None

    current_met = (
        toronto.weather_code in (95, 96, 99)
        and toronto.temperature_2m >= 25.0
        and ottawa.temperature_2m >= 22.0
    )
    previous_met = (
        toronto_previous.weather_code in (95, 96, 99)
        and toronto_previous.temperature_2m >= 25.0
        and ottawa_previous.temperature_2m >= 22.0
    )
    if not _newly_triggered(current_met, previous_met):
        return None

    return _make_event(
        city="Ottawa",
        rule_name="instability_transfer_toronto_to_ottawa",
        alert_level="Internal Predictive Watch",
        message=(
            "Thunderstorms are active in Toronto with warm conditions in Ottawa. "
            "Prepare for severe weather in Ottawa within the next 4 to 5 hours."
        ),
        reading=ottawa,
        triggered_values={
            "toronto_weather_code": toronto.weather_code,
            "toronto_temperature_2m": toronto.temperature_2m,
            "ottawa_temperature_2m": ottawa.temperature_2m,
        },
    )


def continental_heat_pump(
    vancouver: WeatherReading,
    vancouver_previous: WeatherReading | None,
    target: WeatherReading,
) -> NotableEvent | None:
    if vancouver_previous is None or target.city not in ("Toronto", "Ottawa"):
        return None

    current_met = vancouver.temperature_2m >= 26.0
    previous_met = vancouver_previous.temperature_2m >= 26.0
    if not _newly_triggered(current_met, previous_met):
        return None

    return _make_event(
        city=target.city,
        rule_name="continental_heat_pump",
        alert_level="System Informational Flag",
        message=(
            f"Vancouver is unusually warm. {target.city} may see a major heat spike "
            "in 4 to 5 days—plan ahead for cooling and hydration."
        ),
        reading=target,
        triggered_values={
            "vancouver_temperature_2m": vancouver.temperature_2m,
            "flagged_city": target.city,
        },
        event_timestamp=vancouver.timestamp,
    )


def frontal_boundary_flash_flood_trap(
    toronto: WeatherReading,
    toronto_previous: WeatherReading | None,
    ottawa: WeatherReading,
    ottawa_previous: WeatherReading | None,
) -> NotableEvent | None:
    if toronto_previous is None or ottawa_previous is None:
        return None

    current_met = (
        toronto.weather_code in (63, 65)
        and toronto.wind_speed_10m >= 30.0
        and ottawa.precipitation >= 10.0
    )
    previous_met = (
        toronto_previous.weather_code in (63, 65)
        and toronto_previous.wind_speed_10m >= 30.0
        and ottawa_previous.precipitation >= 10.0
    )
    if not _newly_triggered(current_met, previous_met):
        return None

    return _make_event(
        city="Ottawa",
        rule_name="frontal_boundary_flash_flood_trap",
        alert_level="Red Warning",
        message=(
            "Heavy rain is stalled between Toronto and Ottawa. "
            "Ottawa faces elevated flash-flood risk—avoid low-lying areas and basements."
        ),
        reading=ottawa,
        triggered_values={
            "toronto_weather_code": toronto.weather_code,
            "toronto_wind_speed_10m": toronto.wind_speed_10m,
            "ottawa_precipitation": ottawa.precipitation,
        },
    )
