"""Agent handoff demonstration with a structured handoff message.

Implements the structured handoff from chapter 07/02: the handing-off
agent produces an explicit handoff message (what was requested, what was
done, what the receiving agent should do next), and the receiving agent
works only from that message - not the full history.

Content is mocked; no API key required.

Run:
    python examples/handoff_demo.py
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

REQUIRED_FIELDS = ("question", "key_findings", "recommended_structure")


class HandoffState(TypedDict):
    """Shared state: the conversation plus the structured handoff."""

    messages: Annotated[list, add_messages]
    handoff: str


def researcher(state: HandoffState) -> dict:
    """Researcher: do the research, then emit a structured handoff."""
    question = str(
        state["messages"][0].content if state["messages"] else "unknown question"
    )
    handoff = (
        "RESEARCH_COMPLETE\n"
        f"Question: {question}\n"
        "Key findings:\n"
        "- finding 1: agents are loops over tools\n"
        "- finding 2: evaluation gates every change\n"
        "- finding 3: workflows before agents\n"
        "Recommended structure for the answer: findings then trade-offs"
    )
    return {"messages": [("user", handoff)], "handoff": handoff}


def validate_handoff(handoff: str) -> bool:
    """The handoff must carry the required fields, or it is rejected."""
    lowered = handoff.lower()
    return all(field.replace("_", " ") in lowered for field in REQUIRED_FIELDS)


def route(state: HandoffState) -> Literal["writer", "__end__"]:
    """Hand off only on a valid structured handoff message."""
    return "writer" if validate_handoff(state["handoff"]) else "__end__"


def writer(state: HandoffState) -> dict:
    """Writer: work only from the handoff message, not the full history."""
    return {"messages": [("user", "[writer] answer drafted from the handoff.")]}


def build_handoff_graph():
    """Build and compile the researcher -> writer handoff graph."""
    workflow = StateGraph(HandoffState)
    workflow.add_node("researcher", researcher)
    workflow.add_node("writer", writer)

    workflow.add_edge(START, "researcher")
    workflow.add_conditional_edges("researcher", route)
    workflow.add_edge("writer", END)
    return workflow.compile()


# Module-level compiled graph.
agent = build_handoff_graph()


def main() -> None:
    """Run the handoff and verify the structured contract."""
    print("\n=== Structured handoff demo ===\n")

    result = agent.invoke(
        {"messages": [("user", "What matters when building agents?")], "handoff": ""}
    )
    print("Handoff message:")
    print(result["handoff"])

    assert validate_handoff(result["handoff"]), "Handoff failed its own validation"
    assert any("[writer]" in str(m.content) for m in result["messages"]), \
        "Writer never received the handoff"

    # Negative case: an invalid handoff must not transfer control.
    assert not validate_handoff("here is what I found, you take it from here"), \
        "Vague handoff incorrectly accepted"
    print("\nStructured handoff validation passed (positive and negative cases).")


if __name__ == "__main__":
    main()
