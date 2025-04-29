from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_b.weather_client import WeatherClient

app = FastAPI(title="Weather Fetcher Agent")

class WeatherRequest(BaseModel):
    type: str
    location: str

class WeatherResponse(BaseModel):
    location: str
    temperature: float
    condition: str
    humidity: int
    wind_speed: float

@app.post("/", response_model=WeatherResponse)
async def handle_weather_request(request: WeatherRequest) -> Dict[str, Any]:
    """
    Handle weather requests from Agent A
    """
    if request.type != "weather":
        raise HTTPException(status_code=400, detail="Invalid request type")
    
    try:
        # Initialize weather client
        client = WeatherClient()
        
        # Get weather data from MCP server
        weather_data = await client.get_weather(request.location)
        
        # Format response
        return {
            "location": request.location,
            "temperature": weather_data["temperature"],
            "condition": weather_data["condition"],
            "humidity": weather_data["humidity"],
            "wind_speed": weather_data["wind_speed"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003) 