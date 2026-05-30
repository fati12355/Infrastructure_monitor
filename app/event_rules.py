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
            "June storms on the west coast bring heavy rain showers. Because Vancouver "
            "has dense marine traffic and residents out on the water, a sudden convective "
            "burst matching this profile triggers immediate marine and coastal localized "
            "transit safety hazards."
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
            "In late May and early June, the human body has not yet acclimatized to "
            "summer temperatures. A humidex crossing 35°C this early in the year spikes "
            "medical emergencies much faster than the exact same temperature would in August."
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
            "Ottawa's suburban and downtown drainage infrastructure can become easily "
            "overwhelmed by convective spring downpours. Shifting more than 25 mm of "
            "water in a single hour creates flash street pooling and basement flooding risks."
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
            "Late spring convective setups create high-velocity downdrafts. In heavily "
            "treed residential corridors like those in Ottawa and Toronto, these wind "
            "speeds tear down active power grids and tree limbs."
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
            "Severe spring thunderstorms dropping heavy hail onto high-velocity highways "
            "like the 401 instantly reduce traction to near-zero. Because drivers are "
            "traveling at high speeds in summer mindsets, this specific WMO code trigger "
            "requires immediate highway alerts."
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
            "Late spring warm air moving over the still-frigid Pacific waters creates "
            "dense marine advection fog. Stagnant winds keep it locked over the harbor "
            "and airport, completely shutting down visual flight rules (VFR) for "
            "floatplanes and transit."
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
            "When early summer heat builds up in the Ottawa Valley trench without wind "
            "to disperse it, poor air quality and high ground-level ozone concentrations "
            "get trapped. This triggers breathing sensitivities for vulnerable populations "
            "early in the season."
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
            "Severe convective squall lines routinely form over Southwestern Ontario or "
            "Michigan, sweep through Toronto, and race down the spine of Highway 411 and "
            "the St. Lawrence Valley toward Ottawa. Ottawa is already warm and unstable; "
            "severe thunderstorm risk is expected to arrive in 4 to 5 hours."
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
            "Atmospheric blocking ridges often build on the west coast first, causing high "
            "spring temperatures in BC. As the jet stream shifts east, this high-pressure "
            "ridge travels across the Prairies and parks over Eastern Canada roughly 4 to 5 "
            "days later, triggering the first major eastern heatwaves of the year."
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
            "In late spring, slow-moving warm fronts often stall between Toronto and Ottawa. "
            "Both stations are simultaneously registering continuous rain alongside high "
            "precipitation values, indicating a trained atmospheric conveyor belt of "
            "moisture that is not moving. This is the classic setup for major regional "
            "flooding in Eastern Ontario."
        ),
        reading=ottawa,
        triggered_values={
            "toronto_weather_code": toronto.weather_code,
            "toronto_wind_speed_10m": toronto.wind_speed_10m,
            "ottawa_precipitation": ottawa.precipitation,
        },
    )
