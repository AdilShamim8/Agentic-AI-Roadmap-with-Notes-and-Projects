"""Parallel workflow demonstration using LangGraph StateGraph.

Implements fan-out and fan-in parallel evaluation:
1. START fans out into 3 parallel evaluator nodes:
   - eval_depth (depth_score: 0-10)
   - eval_clarity (clarity_score: 0-10)
   - eval_accuracy (accuracy_score: 0-10)
2. Fan-in into an aggregation node that sums scores and determines pass/fail.

Run:
    python examples/parallel_workflow_demo.py
"""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, TypedDict

try:
    from langgraph.graph import END, START, StateGraph
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    START = "__start__"
    END = "__end__"

    class StateGraph:  # type: ignore[no-redef]
        """Lightweight fallback mock for parallel StateGraph execution."""

        def __init__(self, schema: type) -> None:
            self.schema = schema
            self.nodes: Dict[str, Callable[[Any], Dict[str, Any]]] = {}
            self.edges: List[tuple[str, str]] = []

        def add_node(self, key: str, action: Callable[[Any], Dict[str, Any]]) -> None:
            self.nodes[key] = action

        def add_edge(self, start_key: str, end_key: str) -> None:
            self.edges.append((start_key, end_key))

        def compile(self) -> Any:
            return MockParallelCompiledGraph(self.nodes, self.edges)

    class MockParallelCompiledGraph:
        """Executes fan-out nodes and fan-in aggregation nodes."""

        def __init__(self, nodes: Dict[str, Callable[[Any], Dict[str, Any]]], edges: List[tuple[str, str]]) -> None:
            self.nodes = nodes
            self.edges = edges

        def invoke(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
            state = dict(initial_state)
            start_targets = [dst for src, dst in self.edges if src == START]

            for target in start_targets:
                if target in self.nodes:
                    update = self.nodes[target](state)
                    state.update(update)

            remaining_nodes = [name for name in self.nodes if name not in start_targets]
            for node_name in remaining_nodes:
                update = self.nodes[node_name](state)
                state.update(update)

            return state


class EvaluationState(TypedDict):
    """Shared state for parallel evaluators and aggregation."""

    essay: str
    depth_score: int
    clarity_score: int
    accuracy_score: int
    total_score: int
    passed: bool


def eval_depth(state: EvaluationState) -> dict:
    """Evaluate depth of content (0 to 10)."""
    words = len(state["essay"].split())
    score = min(10, max(5, words // 20))
    return {"depth_score": score}


def eval_clarity(state: EvaluationState) -> dict:
    """Evaluate structural clarity (0 to 10)."""
    score = 8 if "\n" in state["essay"] or "." in state["essay"] else 5
    return {"clarity_score": score}


def eval_accuracy(state: EvaluationState) -> dict:
    """Evaluate domain accuracy based on keyword signals."""
    essay_lower = state["essay"].lower()
    technical_keywords = ["state", "graph", "agent", "orchestration", "protocol", "eval"]
    matches = sum(1 for kw in technical_keywords if kw in essay_lower)
    score = min(10, 6 + matches)
    return {"accuracy_score": score}


def aggregate_scores(state: EvaluationState) -> dict:
    """Fan-in aggregator node summing all parallel evaluations."""
    total = state["depth_score"] + state["clarity_score"] + state["accuracy_score"]
    passed = total >= 21
    return {"total_score": total, "passed": passed}


def build_parallel_graph():
    """Build and compile fan-out / fan-in StateGraph."""
    workflow = StateGraph(EvaluationState)

    workflow.add_node("depth", eval_depth)
    workflow.add_node("clarity", eval_clarity)
    workflow.add_node("accuracy", eval_accuracy)
    workflow.add_node("agg", aggregate_scores)

    # Fan-out: START to all 3 evaluators
    workflow.add_edge(START, "depth")
    workflow.add_edge(START, "clarity")
    workflow.add_edge(START, "accuracy")

    # Fan-in: all 3 evaluators to aggregate node
    workflow.add_edge("depth", "agg")
    workflow.add_edge("clarity", "agg")
    workflow.add_edge("accuracy", "agg")
    workflow.add_edge("agg", END)

    return workflow.compile()


pipeline = build_parallel_graph()


def main() -> None:
    """Run parallel evaluators across sample documents."""
    print("\n=== LangGraph Parallel Workflow Demo ===")
    print(f"Engine: {'LangGraph Native' if HAS_LANGGRAPH else 'Standalone Runner (LangGraph Compatible)'}\n")

    sample_essay = (
        "Agentic AI systems rely on deterministic state orchestration using StateGraph architectures. "
        "By decomposing complex workflows into isolated nodes and parallel evaluations, "
        "production teams can enforce protocol verification, track execution latency, and maintain accuracy."
    )

    initial_input: EvaluationState = {
        "essay": sample_essay,
        "depth_score": 0,
        "clarity_score": 0,
        "accuracy_score": 0,
        "total_score": 0,
        "passed": False,
    }

    start_time = time.time()
    result = pipeline.invoke(initial_input)
    elapsed = time.time() - start_time

    print(f"Depth Score:    {result['depth_score']}/10")
    print(f"Clarity Score:  {result['clarity_score']}/10")
    print(f"Accuracy Score: {result['accuracy_score']}/10")
    print(f"Total Score:    {result['total_score']}/30")
    print(f"Passed Gate:    {result['passed']}")
    print(f"Execution Time: {elapsed:.4f}s\n")

    assert result["depth_score"] > 0, "Depth score should be non-zero"
    assert result["clarity_score"] > 0, "Clarity score should be non-zero"
    assert result["accuracy_score"] > 0, "Accuracy score should be non-zero"
    assert result["total_score"] == (result["depth_score"] + result["clarity_score"] + result["accuracy_score"])
    print("Parallel workflow validation completed successfully.")


if __name__ == "__main__":
    main()
