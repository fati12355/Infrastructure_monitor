import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, Response

from app.models import NotableEvent, WeatherReading
from app.poller import poller_loop
from app.storage import Storage

logging.basicConfig(level=logging.INFO)

storage = Storage()
_poller_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _poller_task
    _poller_task = asyncio.create_task(poller_loop(storage))
    yield
    if _poller_task is not None:
        _poller_task.cancel()
        try:
            await _poller_task
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/readings", response_model=list[WeatherReading])
def get_readings(
    response: Response,
    city: str | None = None,
    limit: int = Query(default=50, ge=1),
):
    response.headers["Cache-Control"] = "no-store"
    return storage.list_readings(city=city, limit=limit)


@app.get("/events", response_model=list[NotableEvent])
def get_events(
    response: Response,
    city: str | None = None,
    limit: int = Query(default=50, ge=1),
):
    response.headers["Cache-Control"] = "no-store"
    return storage.list_events(city=city, limit=limit)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
