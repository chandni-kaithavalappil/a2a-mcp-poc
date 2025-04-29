import httpx
from typing import Dict, Any, Optional

class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Makes a request to the MCP server
        
        Args:
            endpoint: The API endpoint to call
            method: HTTP method (GET, POST)
            data: Request data for POST requests
            
        Returns:
            Dict containing the response data
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = await self.client.get(url)
            elif method.upper() == "POST":
                response = await self.client.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            raise Exception(f"HTTP error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"Error making request: {str(e)}")
        
    async def close(self):
        """Closes the HTTP client"""
        await self.client.aclose() 