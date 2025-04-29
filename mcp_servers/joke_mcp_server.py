from fastapi import FastAPI
from pydantic import BaseModel
import random
from typing import Dict, Any

app = FastAPI(title="Joke MCP Server")

class JokeResponse(BaseModel):
    setup: str
    punchline: str
    type: str

# Joke database
JOKES = [
    {
        "setup": "Why don't scientists trust atoms?",
        "punchline": "Because they make up everything!",
        "type": "science"
    },
    {
        "setup": "What did the ocean say to the beach?",
        "punchline": "Nothing, it just waved!",
        "type": "nature"
    },
    {
        "setup": "Why did the scarecrow win an award?",
        "punchline": "Because he was outstanding in his field!",
        "type": "farming"
    },
    {
        "setup": "What do you call a fake noodle?",
        "punchline": "An impasta!",
        "type": "food"
    },
    {
        "setup": "How does a penguin build its house?",
        "punchline": "Igloos it together!",
        "type": "animals"
    }
]

@app.get("/joke", response_model=JokeResponse)
async def get_joke() -> Dict[str, Any]:
    """
    Returns a random joke from the database
    """
    return random.choice(JOKES)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 