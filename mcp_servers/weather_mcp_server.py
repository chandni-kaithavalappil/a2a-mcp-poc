from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
from typing import Dict, Any

app = FastAPI(title="Weather MCP Server")

class WeatherRequest(BaseModel):
    location: str

class WeatherResponse(BaseModel):
    location: str
    temperature: float
    condition: str
    humidity: int
    wind_speed: float

# Supported locations and their weather patterns
LOCATIONS = {
    "New York": {
        "temp_range": (-5, 30),
        "conditions": ["Sunny", "Cloudy", "Rainy", "Snowy"],
        "humidity_range": (30, 80),
        "wind_range": (5, 25)
    },
    "London": {
        "temp_range": (0, 25),
        "conditions": ["Cloudy", "Rainy", "Sunny", "Foggy"],
        "humidity_range": (50, 90),
        "wind_range": (5, 20)
    },
    "Tokyo": {
        "temp_range": (5, 35),
        "conditions": ["Sunny", "Cloudy", "Rainy", "Humid"],
        "humidity_range": (40, 85),
        "wind_range": (5, 15)
    },
    "Paris": {
        "temp_range": (0, 30),
        "conditions": ["Sunny", "Cloudy", "Rainy", "Windy"],
        "humidity_range": (40, 80),
        "wind_range": (5, 20)
    },
    "Sydney": {
        "temp_range": (10, 35),
        "conditions": ["Sunny", "Cloudy", "Rainy", "Windy"],
        "humidity_range": (30, 75),
        "wind_range": (5, 25)
    }
}

@app.post("/weather", response_model=WeatherResponse)
async def get_weather(request: WeatherRequest) -> Dict[str, Any]:
    """
    Returns weather data for a given location
    """
    location = request.location
    if location not in LOCATIONS:
        raise HTTPException(
            status_code=404, 
            detail=f"Weather data not available for {location}. Available cities: {', '.join(LOCATIONS.keys())}"
        )
    
    city_data = LOCATIONS[location]
    
    return {
        "location": location,
        "temperature": round(random.uniform(*city_data["temp_range"]), 1),
        "condition": random.choice(city_data["conditions"]),
        "humidity": random.randint(*city_data["humidity_range"]),
        "wind_speed": round(random.uniform(*city_data["wind_range"]), 1)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 