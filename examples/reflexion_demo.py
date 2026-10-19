"""Reflexion demonstration with a LangGraph StateGraph.

Implements the actor / evaluator / self-reflector loop from chapter 05/03:
1. Actor generates output
2. Evaluator checks it (tests in this demo)
3. Self-reflector produces an explicit, reusable reflection
4. The actor regenerates with the reflection fed back

The actor is a deterministic mock (the chapter shows the LLM version),
so this demo runs without an API key.

Run:
    python examples/reflexion_demo.py
"""

from __future__ import annotations

from operator import add
from typing import Annotated, Literal, TypedDict

from langgraph.graph import START, StateGraph

MAX_ITERATIONS = 3


class ReflexionState(TypedDict):
    """Shared state for the reflexion loop."""

    task: str
    code: str
    test_result: str
    passed: bool
    reflections: Annotated[list[str], add]
    iteration: int


def generate(state: ReflexionState) -> dict:
    """Actor: write code for the task, honoring past reflections (mocked)."""
    iteration = state["iteration"] + 1
    if state["reflections"]:
        # The actor applies the reflection: with feedback present, the
        # second attempt includes the required structure.
        last = state["reflections"][-1]
        code = (
            f"def solve_{state['task']}():\n"
            f"    # applies reflection: {last}\n"
            "    return 42"
        )
    else:
        code = (
            f"# attempt for {state['task']}\n"
            "return 42  # no function defined yet"
        )
    return {"code": code, "iteration": iteration}


def run_tests(state: ReflexionState) -> dict:
    """Evaluator: run the code against the suite (deterministic check)."""
    passed = "def " in state["code"]
    test_result = "passed" if passed else "no function defined"
    return {"passed": passed, "test_result": test_result}


def reflect(state: ReflexionState) -> dict:
    """Self-reflector: produce an explicit, actionable reflection."""
    if state["passed"]:
        return {}
    reflection = (
        "The code failed because no function was defined. Next attempt: "
        "define a named function before returning a value."
    )
    return {"reflections": [reflection]}


def route(state: ReflexionState) -> Literal["generate", "__end__"]:
    """Terminate on evaluator satisfaction or the hard iteration guard."""
    if state["passed"]:
        return "__end__"
    if state["iteration"] >= MAX_ITERATIONS:
        return "__end__"
    return "generate"


def build_reflexion_graph():
    """Build and compile the reflexion StateGraph."""
    workflow = StateGraph(ReflexionState)
    workflow.add_node("generate", generate)
    workflow.add_node("test", run_tests)
    workflow.add_node("reflect", reflect)

    workflow.add_edge(START, "generate")
    workflow.add_edge("generate", "test")
    workflow.add_edge("test", "reflect")
    workflow.add_conditional_edges("reflect", route)

    return workflow.compile()


# Module-level compiled graph.
agent = build_reflexion_graph()


def main() -> None:
    """Run the reflexion loop and verify learning within the cap."""
    print("\n=== Reflexion demo ===\n")
    task = "answer_calc"

    result = agent.invoke(
        {
            "task": task,
            "code": "",
            "test_result": "",
            "passed": False,
            "reflections": [],
            "iteration": 0,
        },
        config={"recursion_limit": 2 * MAX_ITERATIONS + 2},
    )

    print(f"Final code (iteration {result['iteration']}):")
    print(result["code"])
    print(f"\nReflections stored: {result['reflections']}")
    print(f"Tests: {result['test_result']}")

    assert result["passed"], "Evaluator never satisfied within the iteration cap"
    assert result["reflections"], "No reusable reflection was produced"
    print("\nReflexion validation passed.")


if __name__ == "__main__":
    main()
