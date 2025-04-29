import streamlit as st
import httpx
import asyncio
from typing import Dict, Any

# Constants
AGENT_B_URL = "http://localhost:8003"
AGENT_C_URL = "http://localhost:8004"

# Supported cities
CITIES = ["New York", "London", "Tokyo", "Paris", "Sydney"]

async def send_to_agent(agent_url: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Sends a request to an agent and gets the response"""
    async with httpx.AsyncClient() as client:
        response = await client.post(agent_url, json=data)
        return response.json()

def analyze_intent(query: str) -> str:
    """Analyzes user intent based on keywords"""
    query = query.lower()
    if any(word in query for word in ["weather", "temperature", "forecast"]):
        return "weather"
    elif any(word in query for word in ["joke", "funny", "humor"]):
        return "joke"
    return "unknown"

async def process_query(query: str) -> Dict[str, Any]:
    """Processes the user query and gets response from appropriate agent"""
    intent = analyze_intent(query)
    
    if intent == "weather":
        # Extract location from query
        location = "New York"  # Default location
        for city in CITIES:
            if city.lower() in query.lower():
                location = city
                break
                
        try:
            response = await send_to_agent(AGENT_B_URL, {
                "type": "weather",
                "location": location
            })
            return {
                "type": "weather",
                "data": response
            }
        except Exception as e:
            return {
                "type": "error",
                "message": f"Error getting weather data: {str(e)}"
            }
        
    elif intent == "joke":
        try:
            response = await send_to_agent(AGENT_C_URL, {
                "type": "joke"
            })
            return {
                "type": "joke",
                "data": response
            }
        except Exception as e:
            return {
                "type": "error",
                "message": f"Error getting joke: {str(e)}"
            }
        
    else:
        return {
            "type": "error",
            "message": "I don't understand that request. Try asking about weather or tell me a joke!"
        }

def display_response(response: Dict[str, Any]):
    """Displays the response in a user-friendly format"""
    if response["type"] == "weather":
        data = response["data"]
        st.write(f"🌡️ Weather in {data.get('location', 'Unknown')}:")
        st.write(f"Temperature: {data.get('temperature', 'N/A')}°C")
        st.write(f"Condition: {data.get('condition', 'N/A')}")
        st.write(f"Humidity: {data.get('humidity', 'N/A')}%")
        st.write(f"Wind Speed: {data.get('wind_speed', 'N/A')} km/h")
        
    elif response["type"] == "joke":
        data = response["data"]
        st.write("😄 Here's a joke for you:")
        st.write(f"Q: {data.get('setup', 'N/A')}")
        st.write(f"A: {data.get('punchline', 'N/A')}")
        
    else:
        st.error(response["message"])

# Streamlit UI
st.title("🤖 Weather & Jokes POC")
st.write("Ask me about weather in New York, London, Tokyo, Paris, or Sydney, or tell me a joke!")

# Query input
query = st.text_input("What would you like to know?")

if query:
    with st.spinner("Thinking..."):
        response = asyncio.run(process_query(query))
        display_response(response) 