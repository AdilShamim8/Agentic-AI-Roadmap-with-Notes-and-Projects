"""Conversational ReAct agent with persistence and a recursion limit.

This is the minimum viable production agent: it uses create_react_agent,
has a tool, persists state with MemorySaver (swap for PostgresSaver in
production), and caps the run with a recursion limit at invoke time.

Run:
    python examples/conversational_agent_demo.py

Environment:
    ANTHROPIC_API_KEY - required (only when constructing or invoking the
    agent; importing this module never needs a key)
    EXAMPLES_MODEL - optional model override (default: claude-sonnet-5-5)
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Long-lifecycle default; override per environment.
MODEL = os.environ.get("EXAMPLES_MODEL", "claude-sonnet-5-5")


@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location.

    Use this when the user asks about current weather, temperature, or
    conditions. Do not use this for forecasts.

    Args:
        location: City and state/country, e.g. "San Francisco, CA".

    Returns:
        A string like "72F, sunny in San Francisco".
    """
    # In production, call a real weather API here.
    return f"72F, sunny in {location}"


def build_agent() -> CompiledStateGraph:
    """Build the conversational agent.

    Returns a compiled LangGraph agent. The agent is stateless between
    calls unless a thread_id is provided in the config.
    """
    llm = ChatAnthropic(model=MODEL)
    # MemorySaver for dev; use PostgresSaver for production.
    checkpointer = MemorySaver()
    return create_react_agent(llm, tools=[get_weather], checkpointer=checkpointer)


def __getattr__(name: str):
    """Lazily build the module-level agent on first attribute access.

    Importing this module must not require an API key (the eval runner
    and tests import tools from it); constructing the agent does.
    """
    if name == "agent":
        return build_agent()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def main() -> None:
    """Run a two-turn conversation to demonstrate persistence."""
    agent = build_agent()
    config = {
        "configurable": {"thread_id": "demo-001"},
        "recursion_limit": 8,  # safety net: max 8 graph steps per request
    }

    # Turn 1
    print("\n=== Turn 1 ===")
    print("User: What's the weather in San Francisco?")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
        config=config,
    )
    print(f"Agent: {result['messages'][-1].content}")

    # Turn 2 - the agent remembers the previous turn
    print("\n=== Turn 2 ===")
    print("User: What about Tokyo?")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "What about Tokyo?"}]},
        config=config,
    )
    print(f"Agent: {result['messages'][-1].content}")


if __name__ == "__main__":
    main()
