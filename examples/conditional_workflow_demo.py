"""Conditional workflow demonstration using LangGraph StateGraph.

Implements an intent-based routing system:
1. A classification node analyzes incoming customer messages.
2. A conditional edge routes to one of three specialist handlers:
   "refund" -> handle_refund, "bug" -> handle_bug, else -> handle_feature.
3. Each specialist produces a targeted response.

Classification is a mocked keyword heuristic, so no API key is required.

Run:
    python examples/conditional_workflow_demo.py
"""

from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class SupportState(TypedDict):
    """State for support triage and response generation."""

    message: str
    intent: str
    response: str


def classify_message(state: SupportState) -> dict:
    """Classify the incoming message intent based on keyword markers."""
    msg = state["message"].lower()
    refund_words = ["refund", "charge", "charged", "billing", "money back"]
    bug_words = ["error", "crash", "500", "broken", "traceback", "bug", "failing"]
    if any(w in msg for w in refund_words):
        intent = "refund"
    elif any(w in msg for w in bug_words):
        intent = "bug"
    else:
        intent = "feature_request"
    return {"intent": intent}


def handle_refund(state: SupportState) -> dict:
    """Specialized refund handler."""
    return {
        "response": (
            "We have received your billing query. Your transaction "
            "details have been verified, and our financial team will "
            "process the reimbursement within 3-5 business days."
        )
    }


def handle_bug(state: SupportState) -> dict:
    """Specialized bug handler."""
    return {
        "response": (
            "Sorry about the trouble. The engineering team has been "
            "notified, and a ticket has been created. We will follow up "
            "with updates as we diagnose the failure."
        )
    }


def handle_feature(state: SupportState) -> dict:
    """Specialized feature-request handler."""
    return {
        "response": (
            "Thank you for the suggestion. It has been added to the "
            "product backlog, and the product team will evaluate it in "
            "the next planning cycle."
        )
    }


def route(state: SupportState) -> Literal["refund", "bug", "feature", "__end__"]:
    """Route on the structured intent label; never route on the raw message."""
    if state["intent"] == "refund":
        return "refund"
    if state["intent"] == "bug":
        return "bug"
    if state["intent"] == "feature_request":
        return "feature"
    return "__end__"


def build_conditional_graph():
    """Build and compile the support-routing StateGraph."""
    workflow = StateGraph(SupportState)
    workflow.add_node("classify", classify_message)
    workflow.add_node("refund", handle_refund)
    workflow.add_node("bug", handle_bug)
    workflow.add_node("feature", handle_feature)

    workflow.add_edge(START, "classify")
    workflow.add_conditional_edges("classify", route)
    workflow.add_edge("refund", END)
    workflow.add_edge("bug", END)
    workflow.add_edge("feature", END)

    return workflow.compile()


# Module-level compiled graph.
pipeline = build_conditional_graph()


def main() -> None:
    """Run the router over a golden set of labeled messages."""
    print("\n=== Conditional workflow demo ===\n")
    golden = [
        ("I want my money back for order ACME-123", "refund"),
        ("The app crashes when I click login", "bug"),
        ("Can you add a dark mode?", "feature_request"),
        ("How much does the premium plan cost?", "feature_request"),
    ]

    correct = 0
    for message, expected_intent in golden:
        result = pipeline.invoke(
            {"message": message, "intent": "", "response": ""}
        )
        ok = result["intent"] == expected_intent
        correct += ok
        status = "OK " if ok else "MISS"
        print(f"[{status}] {message!r}")
        print(f"       intent={result['intent']} response={result['response'][:60]}")

    accuracy = correct / len(golden)
    print(f"\nRouting accuracy: {accuracy:.0%} ({correct}/{len(golden)})")
    assert accuracy >= 0.75, "Router accuracy below the demo threshold"
    print("Conditional workflow validation passed.")


if __name__ == "__main__":
    main()
