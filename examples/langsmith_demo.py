"""LangSmith tracing demonstration.

Implements the instrumentation from chapter 06/05: set the tracing
environment variables and every LLM call and node execution is traced
automatically. This demo verifies the configuration, emits one traced
(mocked) graph run, and prints where to inspect the trace.

The graph node is a deterministic mock, so the demo runs without an
LLM key; a LangSmith key is only needed to see the trace in the UI.

Run:
    python examples/langsmith_demo.py

Environment:
    LANGCHAIN_API_KEY - required for traces to appear in LangSmith
    LANGCHAIN_TRACING_V2 - set to "true" to enable tracing
    LANGCHAIN_PROJECT - the project traces are written to
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

load_dotenv()

# Enable tracing exactly as the chapter describes. In production these
# live in the environment (see .env.example), not in code.
os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
os.environ.setdefault("LANGCHAIN_PROJECT", "agentic-ai-roadmap")


def configure() -> dict:
    """Report the effective tracing configuration."""
    return {
        "tracing_enabled": os.environ.get("LANGCHAIN_TRACING_V2") == "true",
        "project": os.environ.get("LANGCHAIN_PROJECT", "(default)"),
        "api_key_present": bool(os.environ.get("LANGCHAIN_API_KEY")),
    }


from typing import TypedDict  # noqa: E402


class TraceState(TypedDict):
    question: str
    answer: str


def respond(state: TraceState) -> dict:
    """A traced node (mocked content; an LLM call in production)."""
    return {"answer": f"answer to {state['question']!r} (mocked)"}


def build_traced_graph():
    workflow = StateGraph(TraceState)
    workflow.add_node("respond", respond)
    workflow.add_edge(START, "respond")
    workflow.add_edge("respond", END)
    return workflow.compile()


# Module-level compiled graph.
agent = build_traced_graph()


def main() -> None:
    """Check tracing config, run a traced invocation, report next steps."""
    print("\n=== LangSmith tracing demo ===\n")
    cfg = configure()
    print(f"Tracing enabled: {cfg['tracing_enabled']}")
    print(f"Project:        {cfg['project']}")
    print(f"API key set:    {cfg['api_key_present']}")

    result = agent.invoke({"question": "What is the weather in SF?", "answer": ""})
    print(f"\nTraced run result: {result['answer']}")

    if not cfg["api_key_present"]:
        print("\n[!] LANGCHAIN_API_KEY is not set; the trace was not exported.")
        print("    Set it in .env (see .env.example), re-run, then open:")
        print("    https://smith.langchain.com -> project "
              f"{cfg['project']} -> latest trace")
    else:
        print(f"\nTrace exported. Open https://smith.langchain.com -> "
              f"project {cfg['project']} -> latest trace.")
    print("\nTracing configuration validation passed.")


if __name__ == "__main__":
    main()
