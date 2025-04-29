# A2A + MCP Interoperability POC: Technical Documentation
Git link : https://github.com/chandni-kaithavalappil/a2a-mcp-poc/blob/main/README.md
## Overview
This POC demonstrates the integration of Google's Agent2Agent (A2A) protocol with Anthropic's Model Context Protocol (MCP) through a weather and joke service application. The system showcases how multiple agents can collaborate using A2A while fetching external data through MCP.

## Architecture Components

### 1. Agent2Agent (A2A) Protocol Implementation

#### Core Concepts
- **Agent Communication**: A2A enables direct communication between agents using HTTP/REST protocols
- **Message Passing**: Agents exchange structured JSON messages
- **Intent Routing**: Central agent (Agent A) analyzes and routes requests to specialized agents

#### Implementation Details
```python
# Example of A2A message structure
{
    "type": "weather",  # Intent type
    "location": "New York"  # Parameters
}
```

#### Agent Roles
1. **Agent A (Intent Router)**
   - Implements A2A client using httpx
   - Analyzes user intent using Streamlit
   - Routes requests to appropriate agents
   - Handles response aggregation

2. **Agent B (Weather Fetcher)**
   - Implements A2A server using FastAPI
   - Receives weather requests
   - Communicates with MCP server using httpx
   - Returns formatted responses

3. **Agent C (Joke Teller)**
   - Implements A2A server using FastAPI
   - Receives joke requests
   - Communicates with MCP server using httpx
   - Returns formatted responses

### 2. Model Context Protocol (MCP) Implementation

#### Core Concepts
- **Context Management**: MCP provides structured data access
- **Protocol Standardization**: Consistent API format for data retrieval
- **Service Abstraction**: External services are abstracted through MCP servers

#### Implementation Details
```python
# Example of MCP client implementation
class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None):
        # MCP request handling
```

#### MCP Servers
1. **Weather MCP Server**
   - Provides weather data for supported cities
   - Implements standardized response format using FastAPI
   - Handles city-specific weather patterns

2. **Joke MCP Server**
   - Provides joke data
   - Implements standardized response format using FastAPI
   - Manages joke database

## Communication Flow

### 1. System Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────────────┐
│                              User Interface                             │
│                              (Streamlit)                                │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                │ HTTP/WebSocket
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              Agent A (Router)                           │
│                              (Streamlit + httpx)                        │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                │ A2A Protocol (HTTP/REST)
                                │
                ┌───────────────┴───────────────┐
                │                               │
                ▼                               ▼
┌─────────────────────────┐         ┌─────────────────────────┐
│      Agent B            │         │      Agent C            │
│   (Weather Fetcher)     │         │    (Joke Teller)        │
│   (FastAPI + httpx)     │         │   (FastAPI + httpx)     │
└───────────┬─────────────┘         └───────────┬─────────────┘
            │                                   │
            │ MCP Protocol (HTTP/REST)          │ MCP Protocol (HTTP/REST)
            │                                   │
            ▼                                   ▼
┌─────────────────────────┐         ┌─────────────────────────┐
│   Weather MCP Server    │         │    Joke MCP Server      │
│      (FastAPI)          │         │       (FastAPI)         │
└─────────────────────────┘         └─────────────────────────┘
```

### 2. Weather Request Flow
```
1. User Request (Streamlit)
   ┌─────────────────┐
   │      User       │
   └────────┬────────┘
            │
            ▼
2. Intent Analysis (Agent A)
   ┌─────────────────┐
   │    Agent A      │
   │  (Streamlit)    │
   └────────┬────────┘
            │
            ▼
3. Weather Request (A2A)
   ┌─────────────────┐
   │    Agent B      │
   │   (FastAPI)     │
   └────────┬────────┘
            │
            ▼
4. MCP Request
   ┌─────────────────┐
   │ Weather MCP     │
   │   (FastAPI)     │
   └────────┬────────┘
            │
            ▼
5. Response Flow (A2A)
   ┌─────────────────┐
   │      User       │
   └─────────────────┘
```

### 3. Joke Request Flow
```
1. User Request (Streamlit)
   ┌─────────────────┐
   │      User       │
   └────────┬────────┘
            │
            ▼
2. Intent Analysis (Agent A)
   ┌─────────────────┐
   │    Agent A      │
   │  (Streamlit)    │
   └────────┬────────┘
            │
            ▼
3. Joke Request (A2A)
   ┌─────────────────┐
   │    Agent C      │
   │   (FastAPI)     │
   └────────┬────────┘
            │
            ▼
4. MCP Request
   ┌─────────────────┐
   │  Joke MCP      │
   │   (FastAPI)     │
   └────────┬────────┘
            │
            ▼
5. Response Flow (A2A)
   ┌─────────────────┐
   │      User       │
   └─────────────────┘
```

## Technical Implementation Details

### 1. A2A Protocol Features
- **Asynchronous Communication**: Using `asyncio` and `httpx`
- **Structured Message Format**: JSON-based message structure
- **Error Handling**: HTTP status codes and error messages
- **Service Discovery**: Hardcoded URLs for simplicity

### 2. MCP Protocol Features
- **Standardized Endpoints**: Consistent API structure
- **Data Validation**: Using Pydantic models
- **Error Handling**: HTTP exceptions and custom error messages
- **Response Formatting**: Consistent JSON response structure

### 3. Security Considerations
- Local-only implementation
- No authentication required
- Basic error handling
- Input validation

## Code Structure

```
a2a_mcp_poc/
├── agent_a/              # Intent Router Agent
│   ├── main.py          # Streamlit interface
├── agent_b/             # Weather Fetcher Agent
│   ├── main.py          # A2A server
│   ├── mcp_client.py    # MCP client base
│   └── weather_client.py # Weather-specific client
├── agent_c/             # Joke Teller Agent
│   ├── main.py          # A2A server
│   ├── mcp_client.py    # MCP client base
│   └── joke_client.py   # Joke-specific client
└── mcp_servers/         # MCP Servers
    ├── weather_mcp_server.py
    └── joke_mcp_server.py
```

## Future Enhancements

1. **A2A Improvements**
   - Dynamic service discovery
   - Message queuing
   - Authentication and authorization
   - Load balancing

2. **MCP Improvements**
   - Real API integration
   - Caching layer
   - Rate limiting
   - Data persistence

3. **General Improvements**
   - Containerization
   - Monitoring and logging
   - Automated testing
   - CI/CD pipeline

## Conclusion
This POC successfully demonstrates the integration of A2A and MCP protocols in a practical application. It shows how multiple agents can collaborate using A2A while fetching external data through MCP, providing a foundation for more complex agent-based systems. 