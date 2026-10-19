"""LangGraph Functional API demonstration with @entrypoint, @task, and interrupt.

Demonstrates:
1. @task decorator for checkpointable units of work
2. @entrypoint decorator managing the orchestrator lifecycle
3. interrupt() for pausing execution pending human review
4. Resuming execution with Command(resume=...)

The tasks are mocked content generators, so no API key is required.

Run:
    python examples/functional_api_demo.py
"""

from __future__ import annotations

from typing import Any

from langchain_core.runnables.config import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.func import entrypoint, task
from langgraph.types import Command, interrupt


@task
def research(topic: str) -> str:
    """Pretend to research the topic (mocked; no LLM call)."""
    return f"Key insights, market trends, and architectural standards on {topic}."


@task
def summarize(text: str) -> str:
    """Pretend to summarize the research (mocked; no LLM call)."""
    return f"Executive summary: {text}"


@entrypoint(checkpointer=MemorySaver())
def research_agent(topic: str) -> Any:
    """Orchestrate research, summarization, and a human approval gate."""
    raw = research(topic).result()
    summary = summarize(raw).result()
    approved = interrupt({"summary": summary, "question": "Approve this summary?"})
    if not approved:
        return "Summary rejected by reviewer."
    return f"Approved and published: {summary}"


def main() -> None:
    """Run the entrypoint, pause at the interrupt, then resume."""
    print("\n=== Functional API demo ===\n")

    config: RunnableConfig = {"configurable": {"thread_id": "func-demo-1"}}
    test_topic = "agentic AI in 2026"

    print(f"Step 1: invoking the entrypoint with topic: {test_topic!r}")
    paused = research_agent.invoke(test_topic, config=config)
    # At an interrupt, invoke returns {"__interrupt__": (Interrupt(...),)};
    # the payload for the human is the Interrupt's value.
    payload = paused["__interrupt__"][0].value
    print(f"Step 2: flow paused at interrupt. Payload: {payload}")
    assert "question" in payload or "summary" in payload

    print("\nStep 3: resuming with Command(resume=True)...")
    final_output = research_agent.invoke(Command(resume=True), config=config)
    print(f"  Final output: {final_output}")
    assert "Approved and published" in final_output

    print("\nFunctional API interrupt and resume verified.")


if __name__ == "__main__":
    main()
