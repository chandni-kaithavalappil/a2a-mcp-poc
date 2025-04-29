import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_c.mcp_client import MCPClient
from typing import Dict, Any

class JokeClient(MCPClient):
    def __init__(self):
        super().__init__("http://localhost:8002")
    
    async def get_joke(self) -> Dict[str, Any]:
        """
        Gets a random joke
        
        Returns:
            Dict containing joke setup and punchline
        """
        return await self.make_request(
            endpoint="joke",
            method="GET"
        ) 