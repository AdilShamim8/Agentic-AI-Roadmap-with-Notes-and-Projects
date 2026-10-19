"""Continuous improvement demonstration: feedback, A/B, versioning.

Implements chapter 08/07:
1. Explicit + implicit feedback collection
2. A/B routing between two agent versions
3. Version tagging of every request
4. A rollback decision driven by the scores

Deterministic and keyless.

Run:
    python examples/continuous_improvement_demo.py
"""

from __future__ import annotations

import random

WEIGHTS = {"a": 0.5, "b": 0.5}
VERSIONS = {
    "a": {"prompt": "Answer concisely.", "score": 0.82},
    "b": {"prompt": "Answer thoroughly with citations.", "score": 0.87},
}


def route_request(weights: dict[str, float]) -> str:
    """Route a share of traffic to each version."""
    versions = list(weights)
    chosen = random.choices(versions, weights=[weights[v] for v in versions])[0]
    return chosen


def agent_response(version: str, message: str) -> dict:
    """Produce a tagged response (mocked content per version)."""
    style = VERSIONS[version]["prompt"]
    return {
        "version": version,
        "response": f"[{version}] {style} -> {message[:40]}...",
    }


def collect_feedback(version: str, explicit: str, implicit: str) -> dict:
    """Collect explicit (thumbs) and implicit (re-ask) signals."""
    thumbs_up = explicit == "up"
    re_asked = implicit == "re_asked"
    return {"version": version, "thumbs_up": thumbs_up, "re_asked": re_asked}


def aggregate_scores(feedback: list[dict]) -> dict[str, float]:
    """Score per version: thumbs weighted above re-asks."""
    scores: dict[str, list[float]] = {}
    for f in feedback:
        point = (1.0 if f["thumbs_up"] else 0.0) - (0.5 if f["re_asked"] else 0.0)
        scores.setdefault(f["version"], []).append(point)
    return {v: sum(points) / len(points) for v, points in scores.items()}


def decide_promotion(scores: dict[str, float], baseline: float) -> str:
    """Promote, iterate, or roll back based on the measured scores."""
    best = max(scores, key=lambda v: scores[v])
    if scores[best] >= baseline + 0.05:
        return f"promote {best}"
    if any(score < baseline - 0.10 for score in scores.values()):
        return "roll back"
    return "keep iterating"


def main() -> None:
    """Run the A/B experiment and the promotion decision."""
    print("\n=== Continuous improvement demo ===\n")

    # 1. A/B routing with tagged responses.
    random.seed(19)
    responses = []
    for message in ("What is an agent?", "How do I evaluate one?", "Compare workflows"):
        version = route_request(WEIGHTS)
        responses.append(agent_response(version, message))
    for r in responses:
        print(f"  {r['version']}: {r['response']}")
    assert all(r["version"] in VERSIONS for r in responses), "Untagged response"

    # 2. Feedback collection (explicit + implicit).
    feedback = [
        collect_feedback("a", explicit="up", implicit="ok"),
        collect_feedback("a", explicit="down", implicit="re_asked"),
        collect_feedback("b", explicit="up", implicit="ok"),
        collect_feedback("b", explicit="up", implicit="ok"),
    ]

    # 3. Aggregation and the promotion/rollback decision.
    scores = aggregate_scores(feedback)
    print(f"\nScores: {scores}")
    decision = decide_promotion(scores, baseline=0.75)
    print(f"Decision: {decision}")

    assert decision == "promote b", "The measured winner should be promoted"
    print("\nContinuous improvement checks passed.")


if __name__ == "__main__":
    main()
