"""Retrieval as a tool: scoped search with iterative refinement.

Demonstrates the module 04 retrieval pattern. The retrieval logic is real
and deterministic: the tool ranks a fixed two-tenant corpus and enforces
tenant boundaries inside the tool. The agent decision layer is a scripted
stand-in so the demo runs without API keys (the chapter code block shows
the same loop with a real model).

Run:
    python examples/retrieval_demo.py

Environment:
    none required for the scripted run. ANTHROPIC_API_KEY is only needed
    to build the real agent via build_agent(); importing this module
    never needs a key.
    EXAMPLES_MODEL - optional model override (default: claude-sonnet-5-5)
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Long-lifecycle default; override per environment.
MODEL = os.environ.get("EXAMPLES_MODEL", "claude-sonnet-5-5")

# Two tenants share one tool; each tenant only ever sees its own corpus.
# The loyalty-terms document deliberately avoids the word "refund" so the
# demo's first (broad) query genuinely cannot match it - the
# reformulation in beat 2 is real, not staged.
_KB: dict[str, dict[str, str]] = {
    "acme": {
        "doc-1": (
            "Refund policy: standard customers may request a refund within 30 "
            "days of purchase. Refunds go to the original payment method "
            "within 5 business days."
        ),
        "doc-2": (
            "Loyalty tier benefits: loyalty members may cancel within 90 days "
            "and receive a 10 percent credit on every cancelled order."
        ),
        "doc-3": (
            "Late delivery compensation: when a delivery misses its promised "
            "window, the customer is owed a shipping refund plus a voucher; "
            "for loyalty members the voucher is doubled."
        ),
        "doc-4": "Account management: change plan tiers and billing dates in the settings tab.",
        "doc-5": "Escalation: unresolved tickets go to tier-2 support after 48 hours.",
    },
    "globex": {
        "doc-1": "Globex returns: items can be returned within 14 days of purchase.",
        "doc-2": "Globex support hours: chat support is available 24/7.",
    },
}

_STOPWORDS = frozenset(
    {"the", "a", "an", "for", "of", "to", "and", "in", "on", "is", "how", "do", "i", "what"}
)


def _score(query: str, text: str) -> int:
    """Deterministic term-frequency score; no external service, no keys."""
    terms = [t for t in query.lower().split() if t not in _STOPWORDS]
    words = text.lower().split()
    return sum(words.count(t) for t in terms)


@tool
def search_knowledge_base(query: str, tenant: str = "acme") -> str:
    """Search the customer-support knowledge base for one tenant.

    Use this when the question is about policies, refunds, deliveries, or
    account management. If the first result set does not contain the
    detail you need, reformulate the query and search again.

    Args:
        query: The search query, e.g. "refund policy".
        tenant: The tenant whose knowledge base to search. The tool only
            ever returns documents that belong to this tenant.

    Returns:
        The top matching documents with scores, or a no-match message
        suggesting a reformulation.
    """
    corpus = _KB.get(tenant)
    if corpus is None:
        known = ", ".join(sorted(_KB))
        return f"Unknown tenant {tenant!r}. Known tenants: {known}."

    scored = sorted(
        ((doc_id, _score(query, text), text) for doc_id, text in corpus.items()),
        key=lambda item: item[1],
        reverse=True,
    )
    top = [item for item in scored if item[1] > 0][:3]
    if not top:
        return (
            f"No documents matched {query!r} in the {tenant!r} knowledge base. "
            "Try different terms or a narrower query."
        )

    lines = (
        f"[{i}] {doc_id} (score {score}): {text}"
        for i, (doc_id, score, text) in enumerate(top, 1)
    )
    return "\n".join(lines)


def build_agent():
    """Build the real ReAct agent (requires ANTHROPIC_API_KEY)."""
    llm = ChatAnthropic(model=MODEL)
    return create_react_agent(llm, tools=[search_knowledge_base])


def __getattr__(name: str):
    """Lazily build the module-level agent on first attribute access.

    Importing this module must not require an API key (the eval runner
    and tests import tools from it); constructing the agent does.
    """
    if name == "agent":
        return build_agent()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def _run_tool(query: str, tenant: str) -> str:
    """Invoke the tool the way an agent would and echo the call."""
    print(f"  [tool call] search_knowledge_base(query={query!r}, tenant={tenant!r})")
    result = search_knowledge_base.invoke({"query": query, "tenant": tenant})
    for line in result.splitlines():
        print(f"  [tool result] {line[:100]}")
    return result


def main() -> None:
    """Run the scripted retrieval loop (deterministic stand-in for the LLM)."""
    print("\n=== Retrieval demo ===")
    question = (
        "What are the cancellation terms for a loyalty member, "
        "and what is owed if their delivery is late?"
    )
    print(f"Question: {question}")

    print("\n--- Beat 1: tenant scoping (same query, two tenants) ---")
    _run_tool("refund policy", "acme")
    _run_tool("refund policy", "globex")
    print("  -> The tool returns each tenant's own corpus; no cross-tenant leak.")

    print("\n--- Beat 2: iterative refinement (the demo's point) ---")
    _run_tool("refund policy", "acme")
    # The result covers standard customers only; the loyalty terms document
    # does not contain the word "refund", so no query phrased around
    # refunds can ever match it. A real model reads the result, notices
    # the gap, and reformulates. Here the script does:
    _run_tool("loyalty member benefits", "acme")
    _run_tool("late delivery compensation", "acme")

    print("\n--- Beat 3: failure paths you must handle ---")
    _run_tool("refund policy", "initech")  # unknown tenant
    _run_tool("quantum chromodynamics", "acme")  # no match

    print("\n--- Composed answer ---")
    print("  (scripted synthesis; a real model generates this from the tool results)")
    print("  Cancellation: loyalty members may cancel within 90 days and receive")
    print("  a 10 percent credit on every cancelled order (doc-2).")
    print("  Late delivery: a shipping refund plus a voucher, doubled for loyalty")
    print("  members (doc-3).")
    print("\n=== End retrieval demo ===")


if __name__ == "__main__":
    main()
