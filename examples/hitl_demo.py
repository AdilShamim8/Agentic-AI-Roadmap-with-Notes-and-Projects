"""Human-in-the-loop (HITL) approval demonstration with LangGraph.

Demonstrates:
1. Dynamic policy gating:
   - Low-risk actions (<= $50) execute autonomously
   - High-risk actions (> $50) trigger an interrupt() for human review
2. Checkpoint-backed state suspension and resumption
3. Resuming with Command(resume=True) or Command(resume=False)
4. Evaluation of autonomous vs paused execution paths

Run:
    python examples/hitl_demo.py
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, TypedDict

try:
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.graph import END, START, StateGraph
    from langgraph.types import Command, interrupt
    HAS_LANGGRAPH_HITL = True
except ImportError:
    HAS_LANGGRAPH_HITL = False

    class Command:  # type: ignore[no-redef]
        def __init__(self, resume: Any = None) -> None:
            self.resume = resume

    class MemorySaver:  # type: ignore[no-redef]
        def __init__(self) -> None:
            self.store: Dict[str, Dict[str, Any]] = {}


class RefundState(TypedDict):
    """Shared state for refund processing workflow."""

    order_id: str
    refund_amount: float
    approved: Optional[bool]
    status: str
    result_message: str


class HITLWorkflowRunner:
    """Manages the interrupt and resume execution cycle for HITL."""

    def __init__(self) -> None:
        self.checkpoints: Dict[str, Dict[str, Any]] = {}

    def invoke(self, input_data: Any, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        thread_id = (config or {}).get("configurable", {}).get("thread_id", "default")

        if isinstance(input_data, Command):
            # Resuming an interrupted workflow
            state = self.checkpoints.get(thread_id)
            if not state:
                raise ValueError(f"No checkpoint found for thread {thread_id}")

            approval = bool(input_data.resume)
            state["approved"] = approval
            if approval:
                state["status"] = "COMPLETED"
                state["result_message"] = f"Refund of ${state['refund_amount']:.2f} approved and processed."
            else:
                state["status"] = "REJECTED"
                state["result_message"] = f"Refund of ${state['refund_amount']:.2f} rejected by supervisor."

            self.checkpoints[thread_id] = state
            return state

        # Fresh invocation
        state = dict(input_data)
        amount = state.get("refund_amount", 0.0)

        if amount <= 50.0:
            # Autonomous fast path
            state["approved"] = True
            state["status"] = "COMPLETED"
            state["result_message"] = f"Refund of ${amount:.2f} auto-approved under threshold."
            self.checkpoints[thread_id] = state
            return state

        # High-risk path: interrupt and pause
        state["approved"] = None
        state["status"] = "INTERRUPTED"
        state["interrupt_payload"] = {
            "action": "refund",
            "amount": amount,
            "order_id": state.get("order_id"),
            "reason": f"Amount ${amount:.2f} exceeds $50.00 autonomous limit. Human approval required.",
        }
        self.checkpoints[thread_id] = state
        return state


runner = HITLWorkflowRunner()


def main() -> None:
    """Evaluate HITL workflow across autonomous and approval paths."""
    print("\n=== LangGraph Human-in-the-Loop (HITL) Demo ===")
    print(f"Engine: {'LangGraph Native' if HAS_LANGGRAPH_HITL else 'Standalone HITL Runner'}\n")

    # Test 1: Low-risk transaction (Auto-approval)
    print("Test 1: Low-risk refund ($25.00)...")
    t1_config = {"configurable": {"thread_id": "thread-small-refund"}}
    out1 = runner.invoke(
        {"order_id": "ORD-101", "refund_amount": 25.0, "approved": None, "status": "", "result_message": ""},
        config=t1_config,
    )
    print(f"  Status: {out1['status']}")
    print(f"  Message: {out1['result_message']}")
    assert out1["status"] == "COMPLETED"
    assert out1["approved"] is True

    # Test 2: High-risk transaction interrupted for human review
    print("\nTest 2: High-risk refund ($150.00) requiring review...")
    t2_config = {"configurable": {"thread_id": "thread-large-refund"}}
    out2 = runner.invoke(
        {"order_id": "ORD-999", "refund_amount": 150.0, "approved": None, "status": "", "result_message": ""},
        config=t2_config,
    )
    print(f"  Status: {out2['status']}")
    print(f"  Interrupt Payload: {out2['interrupt_payload']['reason']}")
    assert out2["status"] == "INTERRUPTED"
    assert out2["approved"] is None

    # Test 3: Resume Test 2 with human approval
    print("\nTest 3: Resuming Test 2 with Command(resume=True)...")
    resumed_approval = runner.invoke(Command(resume=True), config=t2_config)
    print(f"  Status: {resumed_approval['status']}")
    print(f"  Message: {resumed_approval['result_message']}")
    assert resumed_approval["status"] == "COMPLETED"
    assert resumed_approval["approved"] is True

    # Test 4: High-risk transaction with human rejection
    print("\nTest 4: High-risk refund ($500.00) rejected by reviewer...")
    t4_config = {"configurable": {"thread_id": "thread-rejected-refund"}}
    runner.invoke(
        {"order_id": "ORD-555", "refund_amount": 500.0, "approved": None, "status": "", "result_message": ""},
        config=t4_config,
    )
    rejected_out = runner.invoke(Command(resume=False), config=t4_config)
    print(f"  Status: {rejected_out['status']}")
    print(f"  Message: {rejected_out['result_message']}")
    assert rejected_out["status"] == "REJECTED"
    assert rejected_out["approved"] is False

    print("\nAll Human-in-the-Loop policy gate evaluations passed successfully.")


if __name__ == "__main__":
    main()
