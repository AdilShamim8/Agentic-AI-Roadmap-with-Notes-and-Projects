"""Iterative workflow demonstration using LangGraph StateGraph.

Implements a generator-critique refinement loop:
1. Generator creates draft content based on topic and feedback
2. Critic evaluates quality and provides actionable critique
3. Conditional edge checks satisfaction or hits loop guard (max_iterations)
4. Evaluates iteration counts and loop termination safety

Run:
    python examples/iterative_workflow_demo.py
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, TypedDict

try:
    from langgraph.graph import END, START, StateGraph
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    START = "__start__"
    END = "__end__"

    class StateGraph:  # type: ignore[no-redef]
        """Lightweight fallback mock for iterative StateGraph loops."""

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
            return MockIterativeCompiledGraph(self.nodes, self.edges, self.conditional_edges)

    class MockIterativeCompiledGraph:
        """Executes iterative loops with support for routing back to generator."""

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
            max_safety_steps = 25
            step_count = 0

            while step_count < max_safety_steps:
                step_count += 1
                if current in self.conditional_edges:
                    next_node = self.conditional_edges[current](state)
                else:
                    targets = [dst for src, dst in self.edges if src == current]
                    next_node = targets[0] if targets else END

                if next_node in (END, "__end__"):
                    break

                current = next_node
                if current in self.nodes:
                    update = self.nodes[current](state)
                    state.update(update)

            return state


class IterativeState(TypedDict):
    """Shared state for generator-critic loop."""

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
        post = f"Most teams miss this about {topic}: deterministic state machines outperform uncontrolled loops. Here is why."
    else:
        post = (
            f"Production blueprint for {topic}:\n"
            f"1. Strict typed schemas for state\n"
            f"2. Deterministic graph routing\n"
            f"3. Automated evaluation gates\n"
            f"Checkpoints keep long-running workflows resilient."
        )

    return {"post": post, "iteration": iteration}


def critique_content(state: IterativeState) -> dict:
    """Critique content for depth and actionable structure."""
    post = state["post"]
    lines = post.splitlines()

    # Criteria: must have at least 2 lines and exceed 60 characters
    if len(lines) >= 3 and len(post) > 60:
        return {"satisfied": True, "feedback": "GOOD: Meets technical depth criteria."}
    return {
        "satisfied": False,
        "feedback": "BAD: Too generic, lacks actionable technical takeaways.",
    }


def should_continue(state: IterativeState) -> str:
    """Decide whether to loop back to generate or terminate."""
    if state["satisfied"]:
        return "__end__"
    if state["iteration"] >= 3:
        return "__end__"  # Safety loop guard
    return "generate"


def build_iterative_graph():
    """Build and compile the iterative refinement StateGraph."""
    workflow = StateGraph(IterativeState)

    workflow.add_node("generate", generate_content)
    workflow.add_node("critique", critique_content)

    workflow.add_edge(START, "generate")
    workflow.add_edge("generate", "critique")
    workflow.add_conditional_edges("critique", should_continue)

    return workflow.compile()


pipeline = build_iterative_graph()


def main() -> None:
    """Run iterative refinement workflow."""
    print("\n=== LangGraph Iterative Workflow Demo ===")
    print(f"Engine: {'LangGraph Native' if HAS_LANGGRAPH else 'Standalone Runner (LangGraph Compatible)'}\n")

    initial_state: IterativeState = {
        "topic": "Agentic AI Orchestration",
        "post": "",
        "feedback": "",
        "satisfied": False,
        "iteration": 0,
    }

    result = pipeline.invoke(initial_state)

    print(f"Total Iterations Taken: {result['iteration']}")
    print(f"Satisfied Quality Gate: {result['satisfied']}")
    print(f"Final Critique Feedback: {result['feedback']}")
    print("\nFinal Optimized Content:\n" + "-" * 40)
    print(result["post"])
    print("-" * 40)

    assert result["iteration"] <= 3, f"Loop guard exceeded: {result['iteration']}"
    assert result["satisfied"] is True, "Failed to reach satisfactory output quality"
    print("\nIterative loop verification completed successfully.")


if __name__ == "__main__":
    main()
