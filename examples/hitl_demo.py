"""Human-in-the-loop (HITL) approval demonstration with LangGraph.

Demonstrates:
1. A risk-threshold policy gate: low-risk actions (<= $50) execute
   autonomously, high-risk actions (> $50) trigger interrupt().
2. Checkpoint-backed suspension and resumption via Command(resume=...).
3. Both approval and rejection paths.

The policy parsing is mocked (no LLM call), so no API key is required.

Run:
    python examples/hitl_demo.py
"""

from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

APPROVAL_THRESHOLD = 50.0


class RefundState(TypedDict):
    """Shared state for the refund approval workflow."""

    order_id: str
    refund_amount: float
    approved: bool | None
    result_message: str


def parse_refund(state: RefundState) -> dict:
    """Extract the refund request (mocked; an LLM would do this in production)."""
    # In production, an LLM call extracts order_id and amount from the
    # conversation. Fixed values keep the demo deterministic.
    return {"refund_amount": 75.0, "order_id": "ACME-123"}


def maybe_approve(state: RefundState) -> dict:
    """Gate: autonomous fast path or human interrupt."""
    if state["refund_amount"] <= APPROVAL_THRESHOLD:
        return {"approved": True}

    approved = interrupt({
        "action": "refund",
        "order_id": state["order_id"],
        "amount": state["refund_amount"],
        "reason": (
            f"Amount exceeds the ${APPROVAL_THRESHOLD:.0f} threshold; "
            "requires human approval."
        ),
    })
    return {"approved": approved}


def execute(state: RefundState) -> dict:
    """Execute the refund or record the rejection."""
    if state["approved"]:
        message = (
            f"Refund of ${state['refund_amount']:.2f} for "
            f"{state['order_id']} processed."
        )
    else:
        message = "Refund cancelled by reviewer."
    return {"result_message": message}


def route(state: RefundState) -> Literal["__end__"]:
    return "__end__"


def build_refund_graph():
    """Build and compile the HITL refund StateGraph."""
    workflow = StateGraph(RefundState)
    workflow.add_node("parse", parse_refund)
    workflow.add_node("gate", maybe_approve)
    workflow.add_node("execute", execute)

    workflow.add_edge(START, "parse")
    workflow.add_edge("parse", "gate")
    workflow.add_edge("gate", "execute")
    workflow.add_edge("execute", END)

    return workflow.compile(checkpointer=MemorySaver())


# Module-level compiled graph.
agent = build_refund_graph()


def main() -> None:
    """Run the approval workflow: pause, approve, and reject paths."""
    print("\n=== HITL demo ===\n")
    config = {"configurable": {"thread_id": "refund-001"}}

    print("Step 1: invoke. The flow pauses at the interrupt.")
    result = agent.invoke(
        {"order_id": "", "refund_amount": 0.0, "approved": None, "result_message": ""},
        config=config,
    )
    print(f"  Interrupt payload shown to the human: {result}")
    assert "__interrupt__" in str(result) or result.get("result_message", "") == ""

    print("\nStep 2: human approves via Command(resume=True).")
    result = agent.invoke(Command(resume=True), config=config)
    print(f"  Result: {result['result_message']}")
    assert "processed" in result["result_message"]

    print("\nStep 3: a second thread rejects via Command(resume=False).")
    config2 = {"configurable": {"thread_id": "refund-002"}}
    agent.invoke(
        {"order_id": "", "refund_amount": 0.0, "approved": None, "result_message": ""},
        config=config2,
    )
    result = agent.invoke(Command(resume=False), config=config2)
    print(f"  Result: {result['result_message']}")
    assert "cancelled" in result["result_message"]

    print("\nHITL interrupt, approval, and rejection verified.")


if __name__ == "__main__":
    main()
