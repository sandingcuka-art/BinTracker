from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# Enable CORS so the frontend can talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Database
SUBURBS = {
    # Gauteng (Pikitup)
    'Braamfontein': {'day': 'Tuesday', 'provider': 'Pikitup'},
    'Sandton': {'day': 'Friday', 'provider': 'Pikitup'},
    'Soweto': {'day': 'Monday', 'provider': 'Pikitup'},
    
    # Western Cape (City of Cape Town)
    'Sea Point': {'day': 'Wednesday', 'provider': 'City of Cape Town'},
    'Gardens': {'day': 'Thursday', 'provider': 'City of Cape Town'},
    'Rondebosch': {'day': 'Tuesday', 'provider': 'City of Cape Town'},
    'Table View': {'day': 'Monday', 'provider': 'City of Cape Town'},
    'Constantia': {'day': 'Friday', 'provider': 'City of Cape Town'},
    'Muizenberg': {'day': 'Monday', 'provider': 'City of Cape Town'},
    'Durbanville': {'day': 'Tuesday', 'provider': 'City of Cape Town'},
    'Somerset West': {'day': 'Wednesday', 'provider': 'City of Cape Town'},
    'Camps Bay': {'day': 'Thursday', 'provider': 'City of Cape Town'},
    'Bellville': {'day': 'Monday', 'provider': 'City of Cape Town'},
}


DAYS_MAP = {
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
    'Friday': 4, 'Saturday': 5, 'Sunday': 6
}

@app.get("/suburbs")
def get_suburbs():
    return list(SUBURBS.keys())

@app.get("/check/{suburb}")
def check_bin(suburb: str):
    if suburb not in SUBURBS:
        return {"error": "Suburb not found"}

    suburb_info = SUBURBS[suburb]
    collection_day_str = suburb_info["day"]
    provider = suburb_info["provider"]
    collection_day_int = DAYS_MAP[collection_day_str]
    
    now = datetime.now()
    current_day_int = now.weekday()
    current_hour = now.hour

    # Calculate days remaining
    days_remaining = (collection_day_int - current_day_int) % 7
    
    status = "Upcoming"
    color = "blue"
    message = f"Next collection is on {collection_day_str}."

    # Logic Engine: The 6 PM Rule & Collection Day logic
    if days_remaining == 0:
        status = "Collected"
        color = "green"
        message = f"{provider} is scheduled for today! Bin should be out."
    
    elif days_remaining == 1 and current_hour >= 18:
        status = "Action Required"
        color = "red"
        message = "Put your bin out tonight! Collection is tomorrow morning."
    
    elif days_remaining == 1:
        status = "Reminder"
        color = "yellow"
        message = "Collection is tomorrow. Get those recycling bags ready!"

    return {
        "suburb": suburb,
        "provider": provider,
        "collection_day": collection_day_str,
        "days_remaining": days_remaining,
        "status": status,
        "message": message,
        "color": color
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
