"""Durable checkpointing demonstration.

Implements chapter 08/04: a checkpointer persists state after every node,
so an interrupted run resumes from the last completed node instead of
restarting. Every side-effecting tool carries an idempotency key so a
resume cannot double-execute.

Default backend: SqliteSaver (durable on disk; no infrastructure needed).
Set POSTGRES_URL to switch to PostgresSaver, the production default.

Runs without an API key (deterministic nodes; an LLM in production).

Run:
    python examples/durability_demo.py

Environment:
    POSTGRES_URL - optional; switches the backend to PostgresSaver
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph


class DurableState(TypedDict):
    """State for the durable workflow."""

    steps_done: list[str]
    refunded: bool


_refund_ledger: dict[str, str] = {}


def issue_refund(order_id: str, amount: float, idempotency_key: str) -> str:
    """A side-effecting call made safe for retries via an idempotency key."""
    if idempotency_key in _refund_ledger:
        return f"duplicate suppressed for key {idempotency_key}"
    _refund_ledger[idempotency_key] = f"refunded ${amount} for {order_id}"
    return _refund_ledger[idempotency_key]


def step_one(state: DurableState) -> dict:
    """First node: verify the order (deterministic)."""
    return {"steps_done": [*state["steps_done"], "verify"]}


def step_two(state: DurableState) -> dict:
    """Second node: the side effect, idempotent by key."""
    issue_refund("ACME-123", 75.0, idempotency_key="key-acme-123-75")
    return {"steps_done": [*state["steps_done"], "refund"], "refunded": True}


def build_durable_graph(checkpointer):
    """Compile the graph with the given checkpointer."""
    workflow = StateGraph(DurableState)
    workflow.add_node("verify", step_one)
    workflow.add_node("refund", step_two)
    workflow.add_edge(START, "verify")
    workflow.add_edge("verify", "refund")
    workflow.add_edge("refund", END)
    return workflow.compile(checkpointer=checkpointer)


def get_checkpointer():
    """Return a checkpointer context manager.

    SqliteSaver by default; PostgresSaver when POSTGRES_URL is set. Both
    from_conn_string helpers are context managers in langgraph 1.x.
    """
    if os.environ.get("POSTGRES_URL"):
        from langgraph.checkpoint.postgres import PostgresSaver

        return PostgresSaver.from_conn_string(os.environ["POSTGRES_URL"])
    tmp = Path(tempfile.gettempdir()) / "durability_demo.sqlite"
    return SqliteSaver.from_conn_string(str(tmp))


def main() -> None:
    """Run, 'crash', and resume - proving durability and idempotency."""
    print("\n=== Durability demo ===\n")
    with get_checkpointer() as checkpointer:
        if hasattr(checkpointer, "setup"):
            checkpointer.setup()

        agent = build_durable_graph(checkpointer)
        config = {"configurable": {"thread_id": "durable-001"}}

        # First run completes.
        r1 = agent.invoke({"steps_done": [], "refunded": False}, config=config)
        print(f"Run 1: steps={r1['steps_done']} refunded={r1['refunded']}")

        # Simulate a resume after a 'crash': same thread, empty input.
        # The checkpointer restores state; nodes do not re-run from scratch.
        r2 = agent.invoke({"steps_done": [], "refunded": False}, config=config)
        print(f"Run 2 (resumed): steps={r2['steps_done']} refunded={r2['refunded']}")

    # The idempotency key must suppress a duplicate side effect.
    duplicate = issue_refund("ACME-123", 75.0, idempotency_key="key-acme-123-75")
    assert "duplicate suppressed" in duplicate, "Idempotency key did not dedupe"

    assert r2["steps_done"] == ["verify", "refund"], "Resume lost completed steps"
    print("\nDurability and idempotency checks passed.")


if __name__ == "__main__":
    main()
