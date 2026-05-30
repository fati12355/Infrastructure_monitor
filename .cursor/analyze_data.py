import sqlite3
import json
from collections import Counter

conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

cursor.execute("""
SELECT city, alert_level
FROM events
""")

rows = cursor.fetchall()

city_counts = Counter()
level_counts = Counter()

for city, level in rows:
    city_counts[city] += 1
    level_counts[level] += 1

result = {
    "events_by_city": dict(city_counts),
    "events_by_level": dict(level_counts),
    "total_events": len(rows)
}

print(json.dumps(result, indent=2))