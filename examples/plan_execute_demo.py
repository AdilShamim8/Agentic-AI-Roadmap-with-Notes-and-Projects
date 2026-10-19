"""Plan-and-execute demonstration with a LangGraph StateGraph.

Implements the three-role pattern from chapter 05/02:
1. Planner: decomposes the goal into steps
2. Executor: runs each step (a ReAct agent in production)
3. Replanner: continues, revises the plan, or declares done

The node bodies are deterministic mocks (the chapter shows the LLM
versions), so this demo runs without an API key.

Run:
    python examples/plan_execute_demo.py
"""

from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import START, StateGraph

MAX_REPLANS = 3


class PlanExecuteState(TypedDict):
    """Shared state for the plan-and-execute loop."""

    goal: str
    plan: list[str]
    results: list[str]
    step_index: int
    done: bool


def planner(state: PlanExecuteState) -> dict:
    """Break the goal into steps (mocked; an LLM call in production)."""
    goal = state["goal"]
    plan = [
        f"Identify the key questions in: {goal}",
        "Gather the evidence for each question",
        "Synthesize the evidence into an answer",
    ]
    return {"plan": plan, "step_index": 0, "results": [], "done": False}


def executor(state: PlanExecuteState) -> dict:
    """Execute the current step (a ReAct agent in production)."""
    step = state["plan"][state["step_index"]]
    result = f"[done] {step}"
    return {
        "results": [*state["results"], result],
        "step_index": state["step_index"] + 1,
    }


def replanner(state: PlanExecuteState) -> dict:
    """Continue, revise, or declare done (mocked decision logic)."""
    if state["step_index"] >= len(state["plan"]):
        return {"done": True}
    # All steps executed in order; the mock never revises.
    return {"done": False}


def route(state: PlanExecuteState) -> Literal["execute", "__end__"]:
    """Route back to the executor until the replanner says done."""
    return "__end__" if state["done"] else "execute"


def build_plan_execute_graph():
    """Build and compile the plan-and-execute StateGraph."""
    workflow = StateGraph(PlanExecuteState)
    workflow.add_node("plan", planner)
    workflow.add_node("execute", executor)
    workflow.add_node("replan", replanner)

    workflow.add_edge(START, "plan")
    workflow.add_edge("plan", "execute")
    workflow.add_edge("execute", "replan")
    workflow.add_conditional_edges("replan", route)

    return workflow.compile()


# Module-level compiled graph.
agent = build_plan_execute_graph()


def main() -> None:
    """Run the planner/executor/replanner loop on a research goal."""
    print("\n=== Plan-and-execute demo ===\n")
    goal = "Write a one-page brief on agentic AI evaluation"
    print(f"Goal: {goal}\n")

    result = agent.invoke(
        {"goal": goal, "plan": [], "results": [], "step_index": 0, "done": False},
        config={"recursion_limit": 2 * MAX_REPLANS + 2},
    )

    print("Plan:")
    for i, step in enumerate(result["plan"], 1):
        print(f"  {i}. {step}")
    print("\nResults:")
    for r in result["results"]:
        print(f"  {r}")

    assert len(result["results"]) == len(result["plan"]), "Not all steps executed"
    assert result["done"], "Replanner never declared done"
    print("\nPlan-and-execute validation passed.")


if __name__ == "__main__":
    main()
