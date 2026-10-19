"""Sequential workflow demonstration using LangGraph StateGraph.

Implements a 3-node sequential pipeline:
1. Outline generation (5-point structure)
2. Essay generation (drafting from outline)
3. Critique generation (3-point review)

Includes evaluation checks validating word counts, structure, and topic
adherence. The "LLM calls" are mocked content generators, so no API key
is required.

Run:
    python examples/sequential_workflow_demo.py
"""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class SequentialState(TypedDict):
    """Shared state across the sequential pipeline."""

    topic: str
    outline: str
    essay: str
    critique: str


def generate_outline(state: SequentialState) -> dict:
    """Generate a structured outline for the given topic."""
    topic = state["topic"]
    outline = (
        f"1. Introduction to {topic}\n"
        f"2. Core architectural principles of {topic}\n"
        "3. Practical implementation and tooling\n"
        "4. Common pitfalls and mitigation strategies\n"
        "5. Production readiness and future outlook"
    )
    return {"outline": outline}


def generate_essay(state: SequentialState) -> dict:
    """Generate an essay based on the outline and topic."""
    topic = state["topic"]
    outline = state["outline"]
    essay = (
        f"The evolution of modern systems has made {topic} a central "
        "discipline in software engineering. When designing robust "
        f"architectures around {topic}, practitioners must first establish "
        "deterministic state boundaries and observable control loops. The "
        f"foundational phase begins with careful planning, as reflected in "
        f"our structured roadmap:\n{outline}\n\n"
        f"In practical deployments of {topic}, engineers frequently "
        "encounter challenges related to latency, cost, and "
        "non-deterministic behavior. By adhering to modular design "
        "patterns and implementing rigorous evaluators at each boundary, "
        "teams ensure high system reliability. Ultimately, mastering "
        f"{topic} requires balancing rapid iteration with enterprise-grade "
        "safeguards and disciplined continuous testing. Through resilient "
        "workflows and systematic error recovery, engineers build "
        "trustworthy and scalable autonomous solutions."
    )
    return {"essay": essay}


def generate_critique(state: SequentialState) -> dict:
    """Generate a 3-point critique of the generated essay."""
    critique = (
        "- Point 1: Solid structural coherence adhering to the 5-point outline.\n"
        "- Point 2: Quantitative benchmarks could reinforce production claims.\n"
        "- Point 3: Error mitigation is well emphasized for reliability."
    )
    return {"critique": critique}


def build_sequential_graph():
    """Build and compile the sequential StateGraph."""
    workflow = StateGraph(SequentialState)
    workflow.add_node("outline", generate_outline)
    workflow.add_node("essay", generate_essay)
    workflow.add_node("critique", generate_critique)

    workflow.add_edge(START, "outline")
    workflow.add_edge("outline", "essay")
    workflow.add_edge("essay", "critique")
    workflow.add_edge("critique", END)

    return workflow.compile()


# Module-level compiled graph.
pipeline = build_sequential_graph()


def evaluate_run(result: SequentialState) -> bool:
    """Evaluate the pipeline output against the chapter criteria.

    - Essay mentions the topic
    - Essay is substantial (80+ words in the demo)
    - Critique contains at least 3 bullet points
    """
    topic_mentioned = result["topic"].lower() in result["essay"].lower()
    word_count = len(result["essay"].split())
    bullet_count = len(
        [line for line in result["critique"].splitlines() if line.strip().startswith("-")]
    )

    assert topic_mentioned, f"Topic '{result['topic']}' not mentioned in essay."
    assert word_count >= 80, f"Essay too short: {word_count} words."
    assert bullet_count >= 3, f"Critique has fewer than 3 bullets: {bullet_count}."
    return True


def main() -> None:
    """Run the sequential workflow on golden test topics."""
    print("\n=== Sequential workflow demo ===")
    test_topics = [
        "Agentic AI orchestration",
        "Deterministic state graphs",
        "Multi-agent communication protocols",
    ]

    for idx, topic in enumerate(test_topics, 1):
        print(f"[{idx}/{len(test_topics)}] Running topic: {topic}")
        output = pipeline.invoke(
            {"topic": topic, "outline": "", "essay": "", "critique": ""}
        )
        evaluate_run(output)
        print(f"  Word count: {len(output['essay'].split())} words")
        print(f"  Critique lines: {len(output['critique'].splitlines())}")
        print("  Evaluation: PASSED\n")

    print("All sequential workflow evaluations passed.")


if __name__ == "__main__":
    main()
