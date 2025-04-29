# A2A + MCP Interoperability POC

This project demonstrates the integration of Google's Agent2Agent (A2A) protocol with Anthropic's Model Context Protocol (MCP) through a simple proof of concept application.

## Project Structure

```
a2a_mcp_poc/
|-- agent_a/              # Intent Router Agent
|   |-- main.py
|-- agent_b/              # Weather Fetcher Agent
|   |-- main.py
|   |-- mcp_client.py
|-- agent_c/              # Joke Teller Agent
|   |-- main.py
|   |-- mcp_client.py
|-- mcp_servers/          # Mock MCP Servers
|   |-- weather_mcp_server.py
|   |-- joke_mcp_server.py
|-- README.md
|-- requirements.txt
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the MCP servers:
```bash
# Terminal 1
python mcp_servers/weather_mcp_server.py

# Terminal 2
python mcp_servers/joke_mcp_server.py
```

4. Start the agents:
```bash
# Terminal 3
python agent_a/main.py

# Terminal 4
python agent_b/main.py

# Terminal 5
python agent_c/main.py
```

5. Access the Streamlit interface:
```bash
streamlit run agent_a/main.py
```

## Architecture

### Agent A (Intent Router)
- Provides a Streamlit interface for user interaction
- Analyzes user intent and delegates tasks to appropriate agents
- Communicates using A2A protocol

### Agent B (Weather Fetcher)
- Handles weather-related queries
- Connects to weather MCP server
- Returns weather information via A2A

### Agent C (Joke Teller)
- Handles joke-related queries
- Connects to joke MCP server
- Returns jokes via A2A

### MCP Servers
- Mock servers providing weather and joke data
- Implemented using FastAPI
- Simulate external API responses

## Communication Flow

1. User sends query via Streamlit interface
2. Agent A analyzes intent and delegates to appropriate agent
3. Agent B/C fetches data via MCP
4. Agent B/C responds to Agent A via A2A
5. Agent A displays final response to user

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Notes

- This is a local-only POC
- Uses mock MCP servers for demonstration
- No authentication required for basic functionality
- Focus on clean delegation and response handling 