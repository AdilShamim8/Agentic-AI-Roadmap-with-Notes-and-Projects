"""Production cost optimization: routing, TTL caches, budgets, eval gates.

Implements chapter 08/05 with the production disciplines added:
- Model routing with a misclassification guard
- Per-tool TTLs set by data volatility
- A per-request token budget derived from the p99 of the eval run
- A monthly budget alert that responds with optimization, not a raise

Deterministic and keyless; every number is illustrative demo data.

Run:
    python examples/cost_optimization_production_demo.py
"""

from __future__ import annotations

import time

# Illustrative demo values; in production, take these from your eval
# report and the provider pricing pages.
EVAL_P99_TOKENS = 3_200
BUDGET_FACTOR = 1.2
REQUEST_BUDGET = int(EVAL_P99_TOKENS * BUDGET_FACTOR)

MONTHLY_BUDGET_USD = 500.0
CURRENT_RUN_RATE_USD = 590.0

PRICE_PER_M = {"cheap-model": 1.00, "expensive-model": 10.00}

TOOL_TTLS = {
    "weather": 600,        # 10 minutes: volatile
    "exchange_rate": 3_600,  # 1 hour: semi-stable
    "document_lookup": None,  # forever: stable
}

_cache: dict[str, tuple[str, float]] = {}


def route_model(question: str) -> str:
    """Difficulty classifier (mocked; a cheap LLM call in production)."""
    complex_markers = ("compare", "analyze", "research", "design", "why")
    lowered = question.lower()
    return "expensive-model" if any(m in lowered for m in complex_markers) else "cheap-model"


def guard_misclassification(question: str, model: str) -> str:
    """Never let a known-complex marker go to the cheap model."""
    if model == "cheap-model" and "compare" in question.lower():
        return "expensive-model"
    return model


def cached_tool(name: str, arg: str) -> str:
    """A tool result served through its per-tool TTL cache."""
    ttl = TOOL_TTLS[name]
    key = f"{name}:{arg}"
    hit = _cache.get(key)
    if hit and (ttl is None or time.time() - hit[1] < ttl):
        return f"{hit[0]} (cache hit, ttl={ttl})"
    value = f"{name}({arg!r}) result"
    _cache[key] = (value, time.time())
    return value


def enforce_request_budget(tokens: int) -> bool:
    """Terminate the request when it exceeds the per-request budget."""
    return tokens <= REQUEST_BUDGET


def respond_to_run_rate() -> str:
    """The monthly-budget rule: optimize first, raise the budget last."""
    if CURRENT_RUN_RATE_USD > MONTHLY_BUDGET_USD:
        return (
            "over budget: optimize first (tighten routing, lower cache "
            "TTLs, cap token budgets); raise the budget only after that"
        )
    return "within budget"


def main() -> None:
    """Exercise all four disciplines."""
    print("\n=== Production cost optimization demo ===\n")

    print(f"Request budget: {REQUEST_BUDGET} tokens "
          f"(p99 {EVAL_P99_TOKENS} + {int((BUDGET_FACTOR - 1) * 100)}%)")
    assert enforce_request_budget(EVAL_P99_TOKENS), "p99 must fit the budget"
    assert not enforce_request_budget(REQUEST_BUDGET + 1), "Budget must cap"

    print("\nRouting with misclassification guard:")
    tricky = "compare RAG with long context"
    routed = guard_misclassification(tricky, route_model(tricky))
    print(f"  {tricky!r} -> {routed}")
    assert routed == "expensive-model", "Guard must catch the misrouted complex item"

    print("\nPer-tool TTL cache:")
    weather = cached_tool("weather", "San Francisco")
    weather_again = cached_tool("weather", "San Francisco")
    doc = cached_tool("document_lookup", "spec-7")
    print(f"  first:  {weather}")
    print(f"  second: {weather_again}")
    print(f"  stable: {doc} (ttl=None means forever)")
    assert "cache hit" in weather_again

    print(f"\nMonthly budget: ${CURRENT_RUN_RATE_USD:.0f} run rate vs "
          f"${MONTHLY_BUDGET_USD:.0f} budget")
    decision = respond_to_run_rate()
    print(f"  -> {decision}")
    assert "optimize first" in decision

    print("\nProduction cost optimization checks passed.")


if __name__ == "__main__":
    main()
