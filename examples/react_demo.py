"""ReAct agent with web search and calculator tools.

Demonstrates the foundational agent pattern: the LLM reasons about what
to do, calls a tool, observes the result, and repeats until it can
answer.

Run:
    python examples/react_demo.py

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
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Long-lifecycle default; override per environment. The 5.x Claude
# generation does not expose temperature - pin the model version and rely
# on the eval suite for stability (see module 06).
MODEL = os.environ.get("EXAMPLES_MODEL", "claude-sonnet-5-5")


@tool
def web_search(query: str) -> str:
    """Search the web for current information.

    Use when the question requires up-to-date information or facts not
    in your training data. Do not use for math (use calculator instead).

    Args:
        query: The search query, e.g. "population of Tokyo 2026".

    Returns:
        A string with the search results.
    """
    # In production, call Tavily, Brave, or another search API.
    return f"[Search results for: {query}]"


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression.

    Use for any arithmetic or calculation. Input should be a valid
    Python expression like '2 + 2' or '13960000 * 2'.

    Args:
        expression: A Python-evaluable math expression.

    Returns:
        The result as a string, or an error message.
    """
    try:
        # Restrict builtins for safety.
        result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def build_agent():
    """Build the ReAct agent."""
    llm = ChatAnthropic(model=MODEL)
    return create_react_agent(llm, tools=[web_search, calculator])


def __getattr__(name: str):
    """Lazily build the module-level agent on first attribute access.

    Importing this module must not require an API key (CI imports tools
    from it); constructing the agent does.
    """
    if name == "agent":
        return build_agent()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def main() -> None:
    """Run a demo question that requires both tools."""
    print("\n=== ReAct demo ===")
    print("Question: What is the population of Tokyo times 2?\n")

    agent = build_agent()
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "What is the population of Tokyo times 2?"}]},
        config={"recursion_limit": 8},  # safety net: max 8 graph steps
    )

    # Print the tool calls and the final answer.
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for call in msg.tool_calls:
                print(f"  [tool call] {call['name']}({call['args']})")
        elif msg.type == "tool":
            print(f"  [tool result] {msg.content[:100]}")
        elif msg.type == "ai" and msg.content:
            print(f"\nFinal answer: {msg.content}")


if __name__ == "__main__":
    main()
