from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SA Bin Collection API",
    description="Check your municipal waste collection schedule by suburb.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


# --- Enums & Constants ---

class Status(str, Enum):
    TODAY = "Today"
    TOMORROW = "Tomorrow - Action Required"
    SOON = "Upcoming"
    REMINDER = "Reminder"


class Color(str, Enum):
    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"
    BLUE = "blue"


DAYS_MAP: dict[str, int] = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2,
    "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6,
}

SUBURBS: dict[str, dict[str, str]] = {
    # Gauteng (Pikitup)
    "Braamfontein":  {"day": "Tuesday",   "provider": "Pikitup"},
    "Sandton":       {"day": "Friday",    "provider": "Pikitup"},
    "Soweto":        {"day": "Monday",    "provider": "Pikitup"},
    # Western Cape (City of Cape Town)
    "Sea Point":     {"day": "Wednesday", "provider": "City of Cape Town"},
    "Gardens":       {"day": "Thursday",  "provider": "City of Cape Town"},
    "Rondebosch":    {"day": "Tuesday",   "provider": "City of Cape Town"},
    "Table View":    {"day": "Monday",    "provider": "City of Cape Town"},
    "Constantia":    {"day": "Friday",    "provider": "City of Cape Town"},
    "Muizenberg":    {"day": "Monday",    "provider": "City of Cape Town"},
    "Durbanville":   {"day": "Tuesday",   "provider": "City of Cape Town"},
    "Somerset West": {"day": "Wednesday", "provider": "City of Cape Town"},
    "Camps Bay":     {"day": "Thursday",  "provider": "City of Cape Town"},
    "Bellville":     {"day": "Monday",    "provider": "City of Cape Town"},
}


# --- Response Models ---

class SuburbsResponse(BaseModel):
    suburbs: list[str]
    total: int


class BinCheckResponse(BaseModel):
    suburb: str
    provider: str
    collection_day: str
    days_remaining: int
    status: str
    message: str
    color: str
    checked_at: str


# --- Helpers ---

def compute_bin_status(
    collection_day_str: str,
    provider: str,
    now: Optional[datetime] = None,
) -> tuple[int, str, str, str]:
    """
    Returns (days_remaining, status, color, message).
    Accepts an optional `now` so logic is fully testable.
    """
    now = now or datetime.now()
    collection_day_int = DAYS_MAP[collection_day_str]
    current_day_int = now.weekday()
    current_hour = now.hour

    days_remaining = (collection_day_int - current_day_int) % 7

    if days_remaining == 0:
        # Already collected today, or collection is today
        if current_hour < 12:
            status = Status.TODAY
            color = Color.GREEN
            message = f"Collection day! Put your bin out now if it isn't already."
        else:
            status = Status.TODAY
            color = Color.GREEN
            message = f"{provider} collects today — bin should already be out."

    elif days_remaining == 1 and current_hour >= 18:
        status = Status.TOMORROW
        color = Color.RED
        message = "Put your bin out tonight — collection is tomorrow morning!"

    elif days_remaining == 1:
        status = Status.REMINDER
        color = Color.YELLOW
        message = "Collection is tomorrow. Get those recycling bags ready!"

    else:
        status = Status.SOON
        color = Color.BLUE
        message = f"Next collection is on {collection_day_str} ({days_remaining} days away)."

    return days_remaining, status, color, message


# --- Routes ---

@app.get("/suburbs", response_model=SuburbsResponse)
def get_suburbs():
    """Return all supported suburbs."""
    names = sorted(SUBURBS.keys())
    return SuburbsResponse(suburbs=names, total=len(names))


@app.get("/check/{suburb}", response_model=BinCheckResponse)
def check_bin(suburb: str):
    """Return the bin collection status for a given suburb."""
    # Case-insensitive lookup
    matched = next(
        (key for key in SUBURBS if key.lower() == suburb.lower()), None
    )
    if matched is None:
        raise HTTPException(
            status_code=404,
            detail=f"Suburb '{suburb}' not found. Use GET /suburbs for the full list.",
        )

    info = SUBURBS[matched]
    days_remaining, status, color, message = compute_bin_status(
        info["day"], info["provider"]
    )

    logger.info("Checked suburb=%s status=%s", matched, status)

    return BinCheckResponse(
        suburb=matched,
        provider=info["provider"],
        collection_day=info["day"],
        days_remaining=days_remaining,
        status=status,
        message=message,
        color=color,
        checked_at=datetime.now().isoformat(),
    )


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    
