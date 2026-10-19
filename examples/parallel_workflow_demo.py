"""Parallel workflow demonstration using LangGraph StateGraph.

Implements fan-out and fan-in parallel evaluation:
1. START fans out into 3 parallel evaluator nodes (depth, clarity,
   accuracy), each scoring 0-10.
2. Fan-in into an aggregation node that sums scores and decides
   pass/fail.

The evaluators are mocked heuristics, so no API key is required.

Run:
    python examples/parallel_workflow_demo.py
"""

from __future__ import annotations

import time
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


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
    """Build and compile the fan-out / fan-in StateGraph."""
    workflow = StateGraph(EvaluationState)

    workflow.add_node("depth", eval_depth)
    workflow.add_node("clarity", eval_clarity)
    workflow.add_node("accuracy", eval_accuracy)
    workflow.add_node("agg", aggregate_scores)

    # Fan-out: START to all 3 evaluators.
    workflow.add_edge(START, "depth")
    workflow.add_edge(START, "clarity")
    workflow.add_edge(START, "accuracy")

    # Fan-in: all 3 evaluators to the aggregator.
    workflow.add_edge("depth", "agg")
    workflow.add_edge("clarity", "agg")
    workflow.add_edge("accuracy", "agg")
    workflow.add_edge("agg", END)

    return workflow.compile()


# Module-level compiled graph.
pipeline = build_parallel_graph()


def main() -> None:
    """Run the parallel evaluators across a sample document."""
    print("\n=== Parallel workflow demo ===\n")

    sample_essay = (
        "Agentic AI systems rely on deterministic state orchestration "
        "using StateGraph architectures. By decomposing complex workflows "
        "into isolated nodes and parallel evaluations, production teams "
        "can enforce protocol verification, track execution latency, and "
        "maintain accuracy."
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

    print(f"Depth score:    {result['depth_score']}/10")
    print(f"Clarity score:  {result['clarity_score']}/10")
    print(f"Accuracy score: {result['accuracy_score']}/10")
    print(f"Total score:    {result['total_score']}/30")
    print(f"Passed gate:    {result['passed']}")
    print(f"Execution time: {elapsed:.4f}s\n")

    assert result["depth_score"] > 0, "Depth score should be non-zero"
    assert result["clarity_score"] > 0, "Clarity score should be non-zero"
    assert result["accuracy_score"] > 0, "Accuracy score should be non-zero"
    expected = result["depth_score"] + result["clarity_score"] + result["accuracy_score"]
    assert result["total_score"] == expected, "Aggregation must sum the three scores"
    print("Parallel workflow validation passed.")


if __name__ == "__main__":
    main()
