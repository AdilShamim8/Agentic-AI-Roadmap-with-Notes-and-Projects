"""Supervisor demonstration with a LangGraph StateGraph.

Implements the supervisor pattern from chapter 05/04: one router
supervises N specialist agents. The supervisor is a router, not a doer;
the specialists do the work and return to the supervisor.

The routing decision is a deterministic mock (the chapter shows the LLM
version), so this demo runs without an API key. The production-grade
implementation is the `langgraph-supervisor` package (see chapter).

Run:
    python examples/supervisor_demo.py
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages

MAX_HANDOFFS = 10


class SupervisorState(TypedDict):
    """Shared state for the supervisor loop."""

    messages: Annotated[list, add_messages]
    next: str


def researcher(state: SupervisorState) -> dict:
    """Research specialist (mocked content; a ReAct agent in production)."""
    return {"messages": [("user", "[researcher] gathered three key findings.")]}


def analyst(state: SupervisorState) -> dict:
    """Analyst specialist (mocked content)."""
    return {"messages": [("user", "[analyst] synthesized the findings into insight.")]}


def writer(state: SupervisorState) -> dict:
    """Writer specialist (mocked content)."""
    return {"messages": [("user", "[writer] drafted the final report.")]}


def supervisor(state: SupervisorState) -> dict:
    """Route to the next specialist, or finish (deterministic mock).

    In production this is a single LLM call that returns the next
    specialist's name or FINISH, given each specialist's one-line
    capability description.
    """
    last = state["messages"][-1].content if state["messages"] else ""
    text = str(last).lower()
    if "[researcher]" in text:
        return {"next": "analyst"}
    if "[analyst]" in text:
        return {"next": "writer"}
    if "[writer]" in text:
        return {"next": "FINISH"}
    return {"next": "researcher"}


def route(state: SupervisorState) -> Literal["researcher", "analyst", "writer", "__end__"]:
    """Map the supervisor's decision onto the graph."""
    if state["next"] == "researcher":
        return "researcher"
    if state["next"] == "analyst":
        return "analyst"
    if state["next"] == "writer":
        return "writer"
    return "__end__"


def build_supervisor_graph():
    """Build and compile the supervisor StateGraph."""
    workflow = StateGraph(SupervisorState)
    workflow.add_node("supervisor", supervisor)
    workflow.add_node("researcher", researcher)
    workflow.add_node("analyst", analyst)
    workflow.add_node("writer", writer)

    workflow.add_edge(START, "supervisor")
    workflow.add_conditional_edges("supervisor", route)
    for specialist in ("researcher", "analyst", "writer"):
        workflow.add_edge(specialist, "supervisor")

    return workflow.compile()


# Module-level compiled graph.
agent = build_supervisor_graph()


def main() -> None:
    """Run a research task through the full handoff chain."""
    print("\n=== Supervisor demo ===\n")
    print("Task: produce a brief on agentic AI evaluation\n")

    result = agent.invoke(
        {"messages": [("user", "Produce a brief on agentic AI evaluation.")], "next": ""},
        config={"recursion_limit": 2 * MAX_HANDOFFS},
    )

    print("Conversation trace:")
    for msg in result["messages"]:
        if hasattr(msg, "content") and msg.content:
            print(f"  {str(msg.content)[:80]}")

    assert any("[writer]" in str(m.content) for m in result["messages"]), \
        "The chain never reached the writer"
    print("\nSupervisor handoff chain validation passed.")


if __name__ == "__main__":
    main()
