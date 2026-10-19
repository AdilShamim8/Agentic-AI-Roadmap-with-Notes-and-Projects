"""Trajectory evaluation demonstration.

Implements the three trajectory checks from chapter 06/04:
1. Tool-call correctness (right tools, right order)
2. Path efficiency (calls made vs. minimum required)
3. No unnecessary tools

Runs against a recorded (mocked) agent trajectory, so no API key is
required. Swap `record_trajectory` for a real agent run in production.

Run:
    python examples/trajectory_eval_demo.py
"""

from __future__ import annotations

from typing import Any


def record_trajectory(agent_call: Any, input_text: str, expected_tools: list[str]) -> dict:
    """Record a trajectory (mocked agent; a real agent in production)."""
    if expected_tools == ["web_search", "calculator"]:
        actual_tools = ["web_search", "calculator"]
    elif expected_tools == ["calculator"]:
        # Deliberately inefficient path: searched before calculating.
        actual_tools = ["web_search", "web_search", "calculator"]
    else:
        actual_tools = list(expected_tools)
    return {
        "input": input_text,
        "expected_tools": expected_tools,
        "actual_tools": actual_tools,
    }


def trajectory_eval(trajectory: dict) -> dict:
    """Evaluate a trajectory: order, coverage, efficiency."""
    expected = trajectory["expected_tools"]
    actual = trajectory["actual_tools"]

    correct_order = actual == expected
    expected_set, actual_set = set(expected), set(actual)
    all_called = expected_set.issubset(actual_set)
    unnecessary = sorted(actual_set - expected_set)
    efficiency = len(expected) / max(len(actual), 1)

    return {
        "correct_order": correct_order,
        "all_called": all_called,
        "unnecessary_tools": unnecessary,
        "efficiency": round(efficiency, 2),
        "actual_tools": actual,
        "expected_tools": expected,
    }


def main() -> None:
    """Evaluate two trajectories: one clean, one inefficient."""
    print("\n=== Trajectory eval demo ===\n")

    t1 = record_trajectory(None, "What is the population of Tokyo times 2?",
                           expected_tools=["web_search", "calculator"])
    r1 = trajectory_eval(t1)
    print("Case 1 (clean path):")
    print(f"  {r1}")
    assert r1["correct_order"] and r1["all_called"] and r1["efficiency"] == 1.0

    t2 = record_trajectory(None, "What is 2+2?",
                           expected_tools=["calculator"])
    r2 = trajectory_eval(t2)
    print("\nCase 2 (wasteful path):")
    print(f"  {r2}")
    assert not r2["correct_order"], "Wasteful path should fail the order check"
    assert r2["unnecessary_tools"] == ["web_search"], "Should flag the extra tool"
    assert r2["efficiency"] < 1.0, "Efficiency should be below 1.0"

    print("\nTrajectory evaluation checks passed.")


if __name__ == "__main__":
    main()
