from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class WeatherReading(BaseModel):
    city: str
    timestamp: datetime
    weather_code: int
    temperature_2m: float
    apparent_temperature: float
    precipitation: float
    wind_speed_10m: float


class NotableEvent(BaseModel):
    city: str
    timestamp: datetime
    rule_name: str
    alert_level: str
    message: str
    reading_timestamp: datetime
    triggered_values: dict[str, Any] = Field(default_factory=dict)
