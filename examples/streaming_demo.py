"""Streaming demonstration with a real LangGraph stream.

Demonstrates:
1. stream_mode="updates": node-level diffs as they happen (UI progress).
2. stream_mode="values": full state after each node (debugging).
3. Time-to-first-event measurement (< 1.0s target).

Token-level streaming (stream_mode="messages") requires an LLM; see
conversational_agent_demo.py. This demo streams a deterministic graph,
so no API key is required.

Run:
    python examples/streaming_demo.py
"""

from __future__ import annotations

import time
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class StreamState(TypedDict):
    """Shared state for the streamed pipeline."""

    question: str
    retrieved: str
    answer: str


def retrieve(state: StreamState) -> dict:
    """Pretend to retrieve context (mocked; no LLM call)."""
    time.sleep(0.05)  # make the stream visible
    return {"retrieved": f"context about {state['question']}"}


def synthesize(state: StreamState) -> dict:
    """Pretend to synthesize an answer (mocked; no LLM call)."""
    time.sleep(0.05)
    return {"answer": f"Answer to {state['question']!r} using {state['retrieved']}."}


def build_stream_graph():
    """Build and compile the streamed StateGraph."""
    workflow = StateGraph(StreamState)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("synthesize", synthesize)
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "synthesize")
    workflow.add_edge("synthesize", END)
    return workflow.compile()


# Module-level compiled graph.
agent = build_stream_graph()


def main() -> None:
    """Stream the graph in both modes and measure time-to-first-event."""
    print("\n=== Streaming demo ===\n")
    question = "What is the weather in SF today?"
    print(f"User query: {question!r}\n")

    print("--- Mode 1: stream_mode='updates' (node diffs, UI progress) ---")
    start = time.time()
    first_event: float | None = None
    for chunk in agent.stream(
        {"question": question, "retrieved": "", "answer": ""},
        stream_mode="updates",
    ):
        if first_event is None:
            first_event = time.time() - start
        for node_name, diff in chunk.items():
            print(f"  [{node_name}] {diff}")
    updates_elapsed = time.time() - start
    print(f"  Stream elapsed: {updates_elapsed:.4f}s\n")

    print("--- Mode 2: stream_mode='values' (full state per step) ---")
    for state in agent.stream(
        {"question": question, "retrieved": "", "answer": ""},
        stream_mode="values",
    ):
        keys = [k for k in state if state.get(k)]
        print(f"  state now has: {keys}")

    print()
    assert first_event is not None and first_event < 1.0, (
        f"Time-to-first-event {first_event} exceeded the 1.0s target"
    )
    print(f"Time-to-first-event: {first_event:.4f}s (target < 1.0s)")
    print("\nStreaming validation passed.")


if __name__ == "__main__":
    main()
