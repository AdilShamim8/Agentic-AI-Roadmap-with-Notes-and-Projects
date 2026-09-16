"""Conditional workflow demonstration using LangGraph StateGraph.

Implements an intent-based routing system:
1. Classification node analyzes incoming customer messages
2. Conditional routing function determines downstream handler:
   - "refund" -> handle_refund
   - "bug" -> handle_bug
   - "feature_request" -> handle_feature
3. Downstream handlers provide targeted responses

Run:
    python examples/conditional_workflow_demo.py
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Literal, TypedDict

try:
    from langgraph.graph import END, START, StateGraph
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    START = "__start__"
    END = "__end__"

    class StateGraph:  # type: ignore[no-redef]
        """Lightweight fallback mock for conditional StateGraph execution."""

        def __init__(self, schema: type) -> None:
            self.schema = schema
            self.nodes: Dict[str, Callable[[Any], Dict[str, Any]]] = {}
            self.edges: List[tuple[str, str]] = []
            self.conditional_edges: Dict[str, Callable[[Any], str]] = {}

        def add_node(self, key: str, action: Callable[[Any], Dict[str, Any]]) -> None:
            self.nodes[key] = action

        def add_edge(self, start_key: str, end_key: str) -> None:
            self.edges.append((start_key, end_key))

        def add_conditional_edges(self, source: str, router: Callable[[Any], str]) -> None:
            self.conditional_edges[source] = router

        def compile(self) -> Any:
            return MockConditionalCompiledGraph(self.nodes, self.edges, self.conditional_edges)

    class MockConditionalCompiledGraph:
        """Executes nodes and evaluates conditional routing functions."""

        def __init__(
            self,
            nodes: Dict[str, Callable[[Any], Dict[str, Any]]],
            edges: List[tuple[str, str]],
            conditional_edges: Dict[str, Callable[[Any], str]],
        ) -> None:
            self.nodes = nodes
            self.edges = edges
            self.conditional_edges = conditional_edges

        def invoke(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
            state = dict(initial_state)
            current = START
            while True:
                if current in self.conditional_edges:
                    next_node = self.conditional_edges[current](state)
                else:
                    targets = [dst for src, dst in self.edges if src == current]
                    next_node = targets[0] if targets else END

                if next_node == END or next_node == "__end__":
                    break

                current = next_node
                if current in self.nodes:
                    update = self.nodes[current](state)
                    state.update(update)

                if current in self.conditional_edges:
                    continue
                targets = [dst for src, dst in self.edges if src == current]
                if not targets or targets[0] in (END, "__end__"):
                    break
                current = targets[0]

            return state


class SupportState(TypedDict):
    """State for support triage and response generation."""

    message: str
    intent: str
    response: str


def classify_message(state: SupportState) -> dict:
    """Classify the incoming message intent based on keyword markers."""
    msg = state["message"].lower()
    if any(w in msg for w in ["refund", "charge", "charged", "billing", "money back", "subscription fee"]):
        intent = "refund"
    elif any(w in msg for w in ["error", "crash", "500", "broken", "traceback", "bug", "failing"]):
        intent = "bug"
    else:
        intent = "feature_request"
    return {"intent": intent}


def handle_refund(state: SupportState) -> dict:
    """Specialized refund handler."""
    return {
        "response": (
            "We have received your billing query. Your transaction details have been verified, "
            "and our financial team will process the reimbursement within 3-5 business days."
        )
    }


def handle_bug(state: SupportState) -> dict:
    """Specialized bug triage handler."""
    return {
        "response": (
            "Thank you for reporting this issue. Our engineering team has created incident ticket "
            "#ENG-8821 with the provided diagnostics to investigate the unexpected behavior."
        )
    }


def handle_feature(state: SupportState) -> dict:
    """Specialized feature request handler."""
    return {
        "response": (
            "Thank you for this suggestion! We have routed your feedback directly to the product team "
            "for consideration in our upcoming quarterly release cycle."
        )
    }


def route_intent(state: SupportState) -> Literal["refund", "bug", "feature", "__end__"]:
    """Conditional router routing to the corresponding specialist node."""
    mapping = {
        "refund": "refund",
        "bug": "bug",
        "feature_request": "feature",
    }
    return mapping.get(state["intent"], "__end__")


def build_conditional_graph():
    """Build and compile the conditional triage StateGraph."""
    workflow = StateGraph(SupportState)

    workflow.add_node("classify", classify_message)
    workflow.add_node("refund", handle_refund)
    workflow.add_node("bug", handle_bug)
    workflow.add_node("feature", handle_feature)

    workflow.add_edge(START, "classify")
    workflow.add_conditional_edges("classify", route_intent)
    workflow.add_edge("refund", END)
    workflow.add_edge("bug", END)
    workflow.add_edge("feature", END)

    return workflow.compile()


pipeline = build_conditional_graph()


def main() -> None:
    """Test conditional triage across test cases."""
    print("\n=== LangGraph Conditional Workflow Demo ===")
    print(f"Engine: {'LangGraph Native' if HAS_LANGGRAPH else 'Standalone Runner (LangGraph Compatible)'}\n")

    test_cases = [
        ("I was accidentally charged twice for my subscription last night", "refund"),
        ("The API returns a 500 internal server error when payload exceeds 2MB", "bug"),
        ("It would be great to have dark mode support and webhook export options", "feature_request"),
    ]

    for idx, (msg, expected_intent) in enumerate(test_cases, 1):
        result = pipeline.invoke({"message": msg, "intent": "", "response": ""})
        print(f"[{idx}/{len(test_cases)}] Message: '{msg}'")
        print(f"  Classified Intent: {result['intent']}")
        print(f"  Routed Response:   {result['response'][:75]}...")
        assert result["intent"] == expected_intent, f"Expected {expected_intent}, got {result['intent']}"
        assert len(result["response"]) > 0, "Response should not be empty"
        print("  Evaluation: PASSED\n")

    print("All conditional workflow tests passed successfully.")


if __name__ == "__main__":
    main()
