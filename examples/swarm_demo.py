"""Swarm demonstration with a LangGraph StateGraph.

Implements the peer-to-peer swarm pattern from chapter 05/05: each agent
hands off directly to any other agent based on its own judgment; there
is no central supervisor.

The handoff decisions are deterministic mocks (the chapter shows the LLM
versions); the production-grade implementation is the `langgraph-swarm`
package (see chapter). Runs without an API key.

Run:
    python examples/swarm_demo.py
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages

MAX_HANDOFFS = 10


class SwarmState(TypedDict):
    """Shared state for the swarm."""

    messages: Annotated[list, add_messages]
    next: str


def researcher(state: SwarmState) -> dict:
    """Research agent. Hands off to the analyst once data is collected."""
    return {
        "messages": [("user", "[researcher] collected the data.")],
        "next": "analyst",
    }


def analyst(state: SwarmState) -> dict:
    """Analyst agent. Hands back for more data or forward to the writer."""
    return {
        "messages": [("user", "[analyst] analysis complete.")],
        "next": "writer",
    }


def writer(state: SwarmState) -> dict:
    """Writer agent. Terminates the swarm when the report is done."""
    return {
        "messages": [("user", "[writer] final report ready.")],
        "next": "FINISH",
    }


def route(state: SwarmState) -> Literal["researcher", "analyst", "writer", "__end__"]:
    """Peer-to-peer routing: each agent's own handoff decision."""
    if state["next"] == "researcher":
        return "researcher"
    if state["next"] == "analyst":
        return "analyst"
    if state["next"] == "writer":
        return "writer"
    return "__end__"


def build_swarm_graph():
    """Build and compile the swarm StateGraph."""
    workflow = StateGraph(SwarmState)
    workflow.add_node("researcher", researcher)
    workflow.add_node("analyst", analyst)
    workflow.add_node("writer", writer)

    workflow.add_edge(START, "researcher")
    workflow.add_conditional_edges("researcher", route)
    workflow.add_conditional_edges("analyst", route)
    workflow.add_conditional_edges("writer", route)

    return workflow.compile()


# Module-level compiled graph.
agent = build_swarm_graph()


def main() -> None:
    """Run the peer-to-peer handoff chain."""
    print("\n=== Swarm demo ===\n")
    print("Task: research, analyze, and write a report\n")

    result = agent.invoke(
        {"messages": [], "next": ""},
        config={"recursion_limit": MAX_HANDOFFS},
    )

    print("Handoff trace:")
    for msg in result["messages"]:
        if hasattr(msg, "content") and msg.content:
            print(f"  {str(msg.content)[:80]}")

    assert any("[writer]" in str(m.content) for m in result["messages"]), \
        "The swarm never reached the writer"
    print("\nSwarm handoff validation passed.")


if __name__ == "__main__":
    main()
