import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_b.mcp_client import MCPClient
from typing import Dict, Any

class WeatherClient(MCPClient):
    def __init__(self):
        super().__init__("http://localhost:8001")
    
    async def get_weather(self, location: str) -> Dict[str, Any]:
        """
        Gets weather information for a specific location
        
        Args:
            location: City name to get weather for
            
        Returns:
            Dict containing weather information
        """
        return await self.make_request(
            endpoint="weather",
            method="POST",
            data={"location": location}
        ) 