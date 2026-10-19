"""Map-reduce demonstration with dynamic fan-out via Send.

Implements the map-reduce pattern from chapter 05/07: fan a batch out
across N items, process each in parallel, and aggregate.

The fan-out uses the real `Send` API (dynamic: the worker count is not
known at graph-definition time). The worker is a deterministic mock
(the chapter shows the LLM version), so this demo runs without an API
key.

Run:
    python examples/map_reduce_demo.py
"""

from __future__ import annotations

from operator import add
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class MapReduceState(TypedDict):
    """Shared state for the batch."""

    documents: list[str]
    summaries: Annotated[list[str], add]
    meta_summary: str


class WorkerState(TypedDict):
    """State handed to a single worker via Send."""

    document: str


def fan_out(state: MapReduceState) -> list[Send]:
    """Dynamic fan-out: one worker invocation per document."""
    return [Send("summarize", {"document": doc}) for doc in state["documents"]]


def summarize(state: WorkerState) -> dict:
    """Summarize one document (mocked; an LLM call in production)."""
    doc = state["document"]
    summary = f"summary of {doc!r} (2 sentences, 12 tokens)"
    return {"summaries": [summary]}


def meta_summarize(state: MapReduceState) -> dict:
    """Reduce: aggregate the per-document summaries (mocked)."""
    joined = "; ".join(state["summaries"])
    return {"meta_summary": f"Meta-summary drawing from {len(state['summaries'])} items: {joined}"}


def build_map_reduce_graph():
    """Build and compile the map-reduce StateGraph with Send fan-out."""
    workflow = StateGraph(MapReduceState)
    workflow.add_node("summarize", summarize)
    workflow.add_node("meta", meta_summarize)

    # Fan-out: dynamic, one worker per document. Fan-in: reducer merge.
    workflow.add_conditional_edges(START, fan_out, ["summarize"])
    workflow.add_edge("summarize", "meta")
    workflow.add_edge("meta", END)
    return workflow.compile()


# Module-level compiled graph.
agent = build_map_reduce_graph()


def main() -> None:
    """Run the batch and verify aggregation."""
    print("\n=== Map-reduce demo ===\n")
    documents = ["doc1 text", "doc2 text", "doc3 text", "doc4 text"]

    result = agent.invoke({"documents": documents, "summaries": [], "meta_summary": ""})

    print(f"Batch size: {len(documents)} (fan-out is dynamic via Send)")
    print("Summaries:")
    for s in result["summaries"]:
        print(f"  {s}")
    print(f"\nMeta-summary: {result['meta_summary']}")

    assert len(result["summaries"]) == len(documents), "Aggregation lost items"
    assert "4 items" in result["meta_summary"], "Meta-summary did not draw from all items"
    print("\nMap-reduce validation passed.")


if __name__ == "__main__":
    main()
