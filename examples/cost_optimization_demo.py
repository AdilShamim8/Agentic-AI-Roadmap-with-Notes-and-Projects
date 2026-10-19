"""Cost optimization demonstration: model routing, token budgets, caching.

Implements the three techniques from chapter 06/06:
1. Model routing: a cheap classifier sends simple requests to a cheap
   model, complex requests to an expensive one
2. Token budgeting: a per-request cap that terminates runaway agents
3. Semantic (TTL) caching of tool results

The router is a deterministic mock (the chapter shows the LLM version),
so this demo runs without an API key.

Run:
    python examples/cost_optimization_demo.py
"""

from __future__ import annotations

import time

TOKEN_BUDGET = 4_000
CACHE_TTL_SECONDS = 600

# Illustrative per-million prices for the demo; use the provider's
# pricing page (https://openai.com/api/pricing) in production.
PRICE_PER_M = {
    "cheap-model": 1.00,
    "expensive-model": 10.00,
}


def route_model(question: str) -> str:
    """Classify difficulty (mocked; a cheap LLM call in production)."""
    complex_markers = ("compare", "analyze", "research", "why", "design")
    lowered = question.lower()
    return "expensive-model" if any(m in lowered for m in complex_markers) else "cheap-model"


_cache: dict[str, tuple[str, float]] = {}


def cached_weather(location: str) -> str:
    """A tool with a TTL cache (10 minutes for weather)."""
    key = f"weather:{location}"
    hit = _cache.get(key)
    if hit and time.time() - hit[1] < CACHE_TTL_SECONDS:
        return f"72F, sunny in {location} (cache hit)"
    result = f"72F, sunny in {location}"
    _cache[key] = (result, time.time())
    return result


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimated request cost in dollars."""
    price = PRICE_PER_M[model]
    return (input_tokens + output_tokens) * price / 1_000_000


def enforce_budget(used_tokens: int) -> bool:
    """Return False (terminate) when the per-request budget is exceeded."""
    return used_tokens <= TOKEN_BUDGET


def main() -> None:
    """Run routing, caching, and budget checks on a small workload."""
    print("\n=== Cost optimization demo ===\n")

    questions = [
        "What is 2+2?",
        "Compare the trade-offs of RAG versus long context windows.",
        "What is 2+3?",
    ]

    total = 0.0
    for q in questions:
        model = route_model(q)
        tokens_in, tokens_out = 800, 200
        within_budget = enforce_budget(tokens_in + tokens_out)
        assert within_budget, "Demo workload should be within budget"
        cost = estimate_cost(model, tokens_in, tokens_out)
        total += cost
        print(f"  {q!r}\n    routed to {model} (~${cost:.5f})")

    print("\nCaching:")
    first = cached_weather("San Francisco")
    second = cached_weather("San Francisco")
    print(f"  first call:  {first}")
    print(f"  second call: {second}")
    assert "cache hit" in second, "TTL cache did not serve the repeat call"

    print(f"\nTotal estimated spend for the workload: ${total:.5f}")
    print(f"Per-request token budget: {TOKEN_BUDGET} (enforced in-line)")
    print("\nCost optimization checks passed.")


if __name__ == "__main__":
    main()
