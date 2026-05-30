from fastapi import FastAPI, Query

from app.models import NotableEvent, WeatherReading
from app.storage import Storage

app = FastAPI()
storage = Storage()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/readings", response_model=list[WeatherReading])
def get_readings(
    city: str | None = None,
    limit: int = Query(default=50, ge=1),
):
    return storage.list_readings(city=city, limit=limit)


@app.get("/events", response_model=list[NotableEvent])
def get_events(
    city: str | None = None,
    limit: int = Query(default=50, ge=1),
):
    return storage.list_events(city=city, limit=limit)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
