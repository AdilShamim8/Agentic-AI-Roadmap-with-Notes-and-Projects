"""Structured outputs and tool calling with Pydantic schemas.

Demonstrates:
- A Pydantic schema for tool arguments
- Retry on validation failure
- A max-iteration limit
- Proper error handling

Run:
    python examples/structured_output_demo.py

Environment:
    ANTHROPIC_API_KEY - required
    EXAMPLES_MODEL - optional model override (default: claude-sonnet-5-5)
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import tool
from pydantic import BaseModel, Field

load_dotenv()

# Long-lifecycle default; override per environment.
MODEL = os.environ.get("EXAMPLES_MODEL", "claude-sonnet-5-5")


class WeatherArgs(BaseModel):
    """Schema for the get_weather tool's arguments."""

    location: str = Field(
        description="City and state/country, e.g. 'San Francisco, CA'. "
        "If the user gives only a city, ask for the country before calling."
    )
    units: str = Field(
        description="'fahrenheit' or 'celsius'. Default to fahrenheit if unspecified."
    )


@tool(args_schema=WeatherArgs)
def get_weather(location: str, units: str = "fahrenheit") -> str:
    """Get the current weather for a location.

    Use this when the user asks about current weather, temperature, or
    conditions. Do not use this for forecasts.

    Returns a string like '72F, sunny'.
    """
    # In production, call a real weather API.
    unit_char = "F" if units.startswith("f") else "C"
    return f"72{unit_char}, sunny in {location}"


def build_agent() -> Runnable:
    """Build an LLM with the weather tool bound."""
    llm = ChatAnthropic(model=MODEL)
    return llm.bind_tools([get_weather])


def run_agent(user_message: str, max_iterations: int = 5) -> str:
    """Run the tool-calling loop with retry and a max-iteration limit.

    Args:
        user_message: The user's question.
        max_iterations: Maximum number of LLM calls before giving up.

    Returns:
        The agent's final response.
    """
    llm = build_agent()
    messages: list = [HumanMessage(content=user_message)]

    for _ in range(max_iterations):
        response = llm.invoke(messages)
        messages.append(response)

        # If the LLM did not call a tool, we are done.
        if not response.tool_calls:
            return response.content

        # Execute each tool call.
        for call in response.tool_calls:
            try:
                result = get_weather.invoke(call["args"])
                messages.append(
                    ToolMessage(content=str(result), tool_call_id=call["id"])
                )
            except Exception as e:
                # Return the error to the LLM so it can recover.
                messages.append(
                    ToolMessage(
                        content=f"Tool call failed: {e}. Try with different arguments.",
                        tool_call_id=call["id"],
                    )
                )

    return "I was unable to complete your request. Please try again."


def main() -> None:
    """Run a demo conversation."""
    print("\n=== Demo 1: simple weather question ===")
    print(run_agent("What's the weather in San Francisco?"))

    print("\n=== Demo 2: with units ===")
    print(run_agent("What's the weather in Celsius in Tokyo?"))


if __name__ == "__main__":
    main()
