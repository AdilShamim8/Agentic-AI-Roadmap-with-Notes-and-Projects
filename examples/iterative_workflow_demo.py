"""Iterative workflow demonstration using LangGraph StateGraph.

Implements a generator-critic refinement loop:
1. Generator creates draft content based on the topic and prior feedback.
2. Critic evaluates quality and produces actionable feedback.
3. A conditional edge routes back to the generator (loop) or to END when
   the critic is satisfied or the max-iteration guard is hit.

Content generation and critique are mocked heuristics, so no API key is
required.

Run:
    python examples/iterative_workflow_demo.py
"""

from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import START, StateGraph

MAX_ITERATIONS = 3


class IterativeState(TypedDict):
    """Shared state for the generator-critic loop."""

    topic: str
    post: str
    feedback: str
    satisfied: bool
    iteration: int


def generate_content(state: IterativeState) -> dict:
    """Generate or revise content based on topic and feedback."""
    iteration = state["iteration"] + 1
    topic = state["topic"]

    if iteration == 1:
        post = f"Exploring {topic} today. Really interesting concepts!"
    elif iteration == 2:
        post = (
            f"Most teams miss this about {topic}: deterministic state "
            "machines outperform uncontrolled loops. Here is why."
        )
    else:
        post = (
            f"Production blueprint for {topic}:\n"
            "1. Strict typed schemas for state\n"
            "2. Deterministic graph routing\n"
            "3. Automated evaluation gates\n"
            "Checkpoints keep long-running workflows resilient."
        )

    return {"post": post, "iteration": iteration}


def critique_content(state: IterativeState) -> dict:
    """Critique content for depth and actionable structure."""
    post = state["post"]
    words = len(post.split())
    has_structure = any(ch in post for ch in ("1.", "2.", ":"))

    if words >= 15 and has_structure:
        satisfied = True
        feedback = ""
    else:
        satisfied = False
        missing = []
        if words < 15:
            missing.append("more depth (15+ words)")
        if not has_structure:
            missing.append("a numbered structure")
        feedback = "Rewrite with: " + ", ".join(missing) + "."

    return {"satisfied": satisfied, "feedback": feedback}


def should_continue(state: IterativeState) -> Literal["generate", "__end__"]:
    """Terminate on critic satisfaction or the hard iteration guard."""
    if state["satisfied"]:
        return "__end__"
    if state["iteration"] >= MAX_ITERATIONS:
        return "__end__"
    return "generate"


def build_iterative_graph():
    """Build and compile the generator-critic StateGraph."""
    workflow = StateGraph(IterativeState)
    workflow.add_node("generate", generate_content)
    workflow.add_node("critique", critique_content)

    workflow.add_edge(START, "generate")
    workflow.add_edge("generate", "critique")
    workflow.add_conditional_edges("critique", should_continue)

    return workflow.compile()


# Module-level compiled graph.
pipeline = build_iterative_graph()


def main() -> None:
    """Run the loop and verify termination behavior."""
    print("\n=== Iterative workflow demo ===\n")
    print(f"Topic: agentic AI in production (max {MAX_ITERATIONS} iterations)\n")

    result = pipeline.invoke(
        {
            "topic": "agentic AI in production",
            "post": "",
            "feedback": "",
            "satisfied": False,
            "iteration": 0,
        }
    )

    print(f"Final post ({result['iteration']} iterations):")
    print(result["post"])
    print(f"\nSatisfied at termination: {result['satisfied']}")

    assert 1 <= result["iteration"] <= MAX_ITERATIONS, "Iteration guard failed"
    print("\nIterative workflow validation passed.")


if __name__ == "__main__":
    main()
