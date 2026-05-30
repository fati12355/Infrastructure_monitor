import json
import sqlite3
from datetime import datetime
from pathlib import Path

from app.models import NotableEvent, WeatherReading


class Storage:
    def __init__(self, db_path: str | Path = "weather.db") -> None:
        self.db_path = Path(db_path)
        self.init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS weather_readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    weather_code INTEGER NOT NULL,
                    temperature_2m REAL NOT NULL,
                    apparent_temperature REAL NOT NULL,
                    precipitation REAL NOT NULL,
                    wind_speed_10m REAL NOT NULL,
                    UNIQUE(city, timestamp)
                );

                CREATE TABLE IF NOT EXISTS notable_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    rule_name TEXT NOT NULL,
                    alert_level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    reading_timestamp TEXT NOT NULL,
                    triggered_values TEXT NOT NULL
                );
                """
            )

    @staticmethod
    def _to_iso(dt: datetime) -> str:
        return dt.isoformat()

    @staticmethod
    def _from_iso(value: str) -> datetime:
        return datetime.fromisoformat(value)

    def _row_to_reading(self, row: sqlite3.Row) -> WeatherReading:
        return WeatherReading(
            city=row["city"],
            timestamp=self._from_iso(row["timestamp"]),
            weather_code=row["weather_code"],
            temperature_2m=row["temperature_2m"],
            apparent_temperature=row["apparent_temperature"],
            precipitation=row["precipitation"],
            wind_speed_10m=row["wind_speed_10m"],
        )

    def _row_to_event(self, row: sqlite3.Row) -> NotableEvent:
        return NotableEvent(
            city=row["city"],
            timestamp=self._from_iso(row["timestamp"]),
            rule_name=row["rule_name"],
            alert_level=row["alert_level"],
            message=row["message"],
            reading_timestamp=self._from_iso(row["reading_timestamp"]),
            triggered_values=json.loads(row["triggered_values"]),
        )

    def reading_exists(self, city: str, timestamp: datetime) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT 1
                FROM weather_readings
                WHERE city = ? AND timestamp = ?
                LIMIT 1
                """,
                (city, self._to_iso(timestamp)),
            ).fetchone()
            return row is not None

    def save_reading(self, reading: WeatherReading) -> bool:
        if self.reading_exists(reading.city, reading.timestamp):
            return False

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO weather_readings (
                    city,
                    timestamp,
                    weather_code,
                    temperature_2m,
                    apparent_temperature,
                    precipitation,
                    wind_speed_10m
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    reading.city,
                    self._to_iso(reading.timestamp),
                    reading.weather_code,
                    reading.temperature_2m,
                    reading.apparent_temperature,
                    reading.precipitation,
                    reading.wind_speed_10m,
                ),
            )
        return True

    def get_latest_reading(self, city: str) -> WeatherReading | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT city, timestamp, weather_code, temperature_2m,
                       apparent_temperature, precipitation, wind_speed_10m
                FROM weather_readings
                WHERE city = ?
                ORDER BY timestamp DESC
                LIMIT 1
                """,
                (city,),
            ).fetchone()

        if row is None:
            return None
        return self._row_to_reading(row)

    def get_reading_before(
        self, city: str, timestamp: datetime
    ) -> WeatherReading | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT city, timestamp, weather_code, temperature_2m,
                       apparent_temperature, precipitation, wind_speed_10m
                FROM weather_readings
                WHERE city = ? AND timestamp < ?
                ORDER BY timestamp DESC
                LIMIT 1
                """,
                (city, self._to_iso(timestamp)),
            ).fetchone()

        if row is None:
            return None
        return self._row_to_reading(row)

    def save_event(self, event: NotableEvent) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO notable_events (
                    city,
                    timestamp,
                    rule_name,
                    alert_level,
                    message,
                    reading_timestamp,
                    triggered_values
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.city,
                    self._to_iso(event.timestamp),
                    event.rule_name,
                    event.alert_level,
                    event.message,
                    self._to_iso(event.reading_timestamp),
                    json.dumps(event.triggered_values),
                ),
            )

    def list_readings(
        self, city: str | None = None, limit: int = 50
    ) -> list[WeatherReading]:
        query = """
            SELECT city, timestamp, weather_code, temperature_2m,
                   apparent_temperature, precipitation, wind_speed_10m
            FROM weather_readings
        """
        params: list[str | int] = []
        if city is not None:
            query += " WHERE city = ?"
            params.append(city)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        return [self._row_to_reading(row) for row in rows]

    def list_events(
        self, city: str | None = None, limit: int = 50
    ) -> list[NotableEvent]:
        query = """
            SELECT city, timestamp, rule_name, alert_level, message,
                   reading_timestamp, triggered_values
            FROM notable_events
        """
        params: list[str | int] = []
        if city is not None:
            query += " WHERE city = ?"
            params.append(city)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()

        return [self._row_to_event(row) for row in rows]
