"""Hierarchical multi-agent demonstration with nested subgraphs.

Implements the three-level hierarchy from chapter 05/06: a top-level
supervisor routes to mid-level team supervisors, each of which routes to
its own specialists. Subgraphs are composed as nodes - the same
mechanism `langgraph-supervisor`'s create_supervisor uses under the hood
(see chapter).

Routing decisions are deterministic mocks (LLM calls in production), so
this demo runs without an API key.

Run:
    python examples/hierarchical_demo.py
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


class HierarchyState(TypedDict):
    """Shared state across all levels."""

    messages: Annotated[list, add_messages]
    next: str


def web_researcher(state: HierarchyState) -> dict:
    """Leaf specialist (mocked content)."""
    return {"messages": [("user", "[web_researcher] web findings ready.")], "next": "FINISH"}


def db_researcher(state: HierarchyState) -> dict:
    """Leaf specialist (mocked content)."""
    return {"messages": [("user", "[db_researcher] database findings ready.")], "next": "FINISH"}


def report_writer(state: HierarchyState) -> dict:
    """Leaf specialist (mocked content)."""
    return {"messages": [("user", "[report_writer] report drafted.")], "next": "FINISH"}


def summary_writer(state: HierarchyState) -> dict:
    """Leaf specialist (mocked content)."""
    return {"messages": [("user", "[summary_writer] summary drafted.")], "next": "FINISH"}


def research_router(state: HierarchyState) -> Literal["web_researcher", "db_researcher", "__end__"]:
    """Mid-level routing (mocked: alternate by turn count parity)."""
    turns = len(state["messages"])
    return "db_researcher" if turns % 2 else "web_researcher"


def writing_router(state: HierarchyState) -> Literal["report_writer", "summary_writer", "__end__"]:
    """Mid-level routing (mocked: reports by default)."""
    return "report_writer"


def build_research_team():
    """Compile the research team subgraph."""
    team = StateGraph(HierarchyState)
    team.add_node("web_researcher", web_researcher)
    team.add_node("db_researcher", db_researcher)
    # One hop: the router (from START) picks the specialist; the leaf ends.
    team.add_conditional_edges(START, research_router, ["web_researcher", "db_researcher"])
    team.add_edge("web_researcher", END)
    team.add_edge("db_researcher", END)
    return team.compile()


def build_writing_team():
    """Compile the writing team subgraph."""
    team = StateGraph(HierarchyState)
    team.add_node("report_writer", report_writer)
    team.add_node("summary_writer", summary_writer)
    # One hop: the router (from START) picks the specialist; the leaf ends.
    team.add_conditional_edges(START, writing_router, ["report_writer", "summary_writer"])
    team.add_edge("report_writer", END)
    team.add_edge("summary_writer", END)
    return team.compile()


def top_supervisor(state: HierarchyState) -> dict:
    """Top-level routing (mocked: research first, then writing, then done).

    Checks are ordered so each marker matches at most one phase: writing
    markers win over research markers, otherwise the research marker
    would route to the writing team forever.
    """
    text = " ".join(str(m.content) for m in state["messages"])
    has_research = "[web_researcher]" in text or "[db_researcher]" in text
    has_writing = "[report_writer]" in text or "[summary_writer]" in text
    if has_writing:
        return {"next": "FINISH"}
    if has_research:
        return {"next": "writing_team"}
    return {"next": "research_team"}


def top_route(state: HierarchyState) -> Literal["research_team", "writing_team", "__end__"]:
    if state["next"] == "research_team":
        return "research_team"
    if state["next"] == "writing_team":
        return "writing_team"
    return "__end__"


def build_hierarchical_graph():
    """Compose the two team subgraphs under a top-level supervisor."""
    workflow = StateGraph(HierarchyState)
    workflow.add_node("supervisor", top_supervisor)
    workflow.add_node("research_team", build_research_team())
    workflow.add_node("writing_team", build_writing_team())

    workflow.add_edge(START, "supervisor")
    workflow.add_conditional_edges("supervisor", top_route)
    workflow.add_edge("research_team", "supervisor")
    workflow.add_edge("writing_team", "supervisor")
    return workflow.compile()


# Module-level compiled graph.
agent = build_hierarchical_graph()


def main() -> None:
    """Run the three-level hierarchy end to end."""
    print("\n=== Hierarchical demo ===\n")

    result = agent.invoke(
        {"messages": [("user", "Research and write up the findings.")], "next": ""},
        config={"recursion_limit": 25},  # subgraph steps count against this
    )

    print("Trace:")
    for msg in result["messages"]:
        if hasattr(msg, "content") and msg.content:
            print(f"  {str(msg.content)[:80]}")

    assert any("[report_writer]" in str(m.content) for m in result["messages"]), \
        "Hierarchy never reached the writing team"
    print("\nHierarchical routing validation passed.")


if __name__ == "__main__":
    main()
