from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_c.joke_client import JokeClient

app = FastAPI(title="Joke Teller Agent")

class JokeRequest(BaseModel):
    type: str

class JokeResponse(BaseModel):
    setup: str
    punchline: str
    type: str

@app.post("/", response_model=JokeResponse)
async def handle_joke_request(request: JokeRequest) -> Dict[str, Any]:
    """
    Handle joke requests from Agent A
    """
    if request.type != "joke":
        raise HTTPException(status_code=400, detail="Invalid request type")
    
    try:
        # Initialize joke client
        client = JokeClient()
        
        # Get joke from MCP server
        joke_data = await client.get_joke()
        
        # Format response
        return {
            "setup": joke_data["setup"],
            "punchline": joke_data["punchline"],
            "type": joke_data["type"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004) 