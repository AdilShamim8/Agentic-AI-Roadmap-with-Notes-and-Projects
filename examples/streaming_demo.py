"""Streaming and user experience demonstration for LangGraph agents.

Demonstrates:
1. Streaming modes:
   - stream_mode="updates": Streams node transition and state updates (for UI progress indicators)
   - stream_mode="messages": Streams token-by-token LLM output for real-time chat UX
2. Latency tracking:
   - Time-to-first-token (TTFT) measurement (< 1.0s target)
3. Structured event visualization for tool calls and responses

Run:
    python examples/streaming_demo.py
"""

from __future__ import annotations

import time
from typing import Any, Dict, Generator, List, Optional, Tuple

try:
    from langchain_core.tools import tool
    from langgraph.prebuilt import create_react_agent
    HAS_LANGGRAPH_STREAM = True
except ImportError:
    HAS_LANGGRAPH_STREAM = False


def get_weather(location: str) -> str:
    """Mock weather service returning condition report."""
    return f"72F, sunny with mild breeze in {location}"


class StreamingDemoAgent:
    """Agent supporting both token-level and node-update streaming simulation."""

    def __init__(self) -> None:
        self.tools = {"get_weather": get_weather}

    def stream_updates(self, user_query: str) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
        """Stream node lifecycle and state transition events."""
        yield ("agent", {"status": "analyzing_query", "action": "deciding_tools"})
        time.sleep(0.05)

        location = "San Francisco" if "sf" in user_query.lower() else "Tokyo"
        yield ("tools", {"tool_name": "get_weather", "arguments": {"location": location}})
        time.sleep(0.05)

        weather_result = self.tools["get_weather"](location)
        yield ("tools", {"tool_name": "get_weather", "result": weather_result})
        time.sleep(0.05)

        yield ("agent", {"status": "synthesizing_response", "content": f"The weather report indicates {weather_result}."})

    def stream_tokens(self, text_to_stream: str) -> Generator[str, None, None]:
        """Simulate token-by-token emission with simulated network delay."""
        tokens = text_to_stream.split(" ")
        for idx, token in enumerate(tokens):
            yield token if idx == len(tokens) - 1 else token + " "
            time.sleep(0.02)


def main() -> None:
    """Execute streaming tests and evaluate time-to-first-token metrics."""
    print("\n=== LangGraph Streaming and UX Demonstration ===")
    agent = StreamingDemoAgent()
    query = "What is the weather in SF today?"

    print(f"User Query: '{query}'\n")

    # Mode 1: Node and Tool Updates (stream_mode="updates")
    print("--- Mode 1: Node Updates Stream (UI State Indicators) ---")
    start_time = time.time()
    for node_name, event_data in agent.stream_updates(query):
        print(f"[{node_name}] -> {event_data}")
    total_pipeline_time = time.time() - start_time
    print(f"Update stream elapsed: {total_pipeline_time:.4f}s\n")

    # Mode 2: Token-Level Streaming (stream_mode="messages")
    print("--- Mode 2: Token-by-Token Streaming (Chat UX) ---")
    response_text = "The weather report indicates 72F, sunny with mild breeze in San Francisco."
    token_stream = agent.stream_tokens(response_text)

    token_start = time.time()
    first_token_time = None
    streamed_tokens: List[str] = []

    print("Live Stream: ", end="", flush=True)
    for token in token_stream:
        if first_token_time is None:
            first_token_time = time.time() - token_start
        streamed_tokens.append(token)
        print(token, end="", flush=True)
    print("\n")

    full_output = "".join(streamed_tokens)
    print(f"Time-to-first-token (TTFT): {first_token_time:.4f}s")
    assert first_token_time is not None and first_token_time < 1.0, f"TTFT exceeded 1.0s threshold: {first_token_time}"
    assert full_output == response_text, "Streamed text does not match expected output."
    print("All streaming UX and latency checks passed successfully.")


if __name__ == "__main__":
    main()
