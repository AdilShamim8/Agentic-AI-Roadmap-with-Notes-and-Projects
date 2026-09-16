"""LangGraph Functional API demonstration with @entrypoint, @task, and interrupt.

Demonstrates:
1. @task decorator for checkpointable discrete units of work
2. @entrypoint decorator for managing the orchestrator lifecycle
3. interrupt() for pausing execution for human review
4. Resuming execution using Command(resume=True)

Run:
    python examples/functional_api_demo.py
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

try:
    from langchain_core.messages import BaseMessage
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.func import entrypoint, task
    from langgraph.types import Command, interrupt
    HAS_LANGGRAPH_FUNC = True
except ImportError:
    HAS_LANGGRAPH_FUNC = False

    class TaskResult:
        """Wrapper for simulated task execution result."""

        def __init__(self, value: Any) -> None:
            self._value = value

        def result(self) -> Any:
            return self._value

    def task(fn: Callable[..., Any]) -> Callable[..., TaskResult]:  # type: ignore[no-redef]
        def wrapper(*args: Any, **kwargs: Any) -> TaskResult:
            return TaskResult(fn(*args, **kwargs))
        return wrapper

    class Command:  # type: ignore[no-redef]
        def __init__(self, resume: Any = None) -> None:
            self.resume = resume

    class MockMemorySaver:
        def __init__(self) -> None:
            self.store: Dict[str, Dict[str, Any]] = {}

    def entrypoint(checkpointer: Any = None) -> Callable[..., Any]:  # type: ignore[no-redef]
        def decorator(fn: Callable[..., Any]) -> Any:
            saver = checkpointer or MockMemorySaver()

            class EntrypointRunner:
                def invoke(self, arg: Any, config: Optional[Dict[str, Any]] = None) -> Any:
                    thread_id = (config or {}).get("configurable", {}).get("thread_id", "default")
                    saved_state = saver.store.get(thread_id, {})

                    if isinstance(arg, Command):
                        # Resuming interrupted state
                        return fn(saved_state.get("topic", ""), resumed_approval=arg.resume)

                    # Initial run: runs up to interrupt
                    saver.store[thread_id] = {"topic": arg}
                    return {
                        "summary": (
                            f"Research synthesis on {arg}: Comprehensive analysis of architectural patterns, "
                            f"tool protocols, and production deployment."
                        ),
                        "question": "Approve this summary?",
                        "status": "INTERRUPTED",
                    }

            return EntrypointRunner()
        return decorator


if HAS_LANGGRAPH_FUNC:
    @task
    def research(topic: str) -> str:
        return f"Key insights, market trends, and architectural standards on {topic}."

    @task
    def summarize(text: str) -> str:
        return f"Executive Summary: {text}"

    @entrypoint(checkpointer=MemorySaver())
    def research_agent(topic: str) -> Any:
        raw = research(topic).result()
        summary = summarize(raw).result()
        approved = interrupt({"summary": summary, "question": "Approve this summary?"})
        if not approved:
            return "Summary rejected by reviewer."
        return f"Approved and Published: {summary}"
else:
    @task
    def research(topic: str) -> str:
        return f"Key insights, market trends, and architectural standards on {topic}."

    @task
    def summarize(text: str) -> str:
        return f"Executive Summary: {text}"

    def standalone_agent_logic(topic: str, resumed_approval: Optional[bool] = None) -> Any:
        raw = research(topic).result()
        summary = summarize(raw).result()
        if resumed_approval is None:
            return {
                "summary": summary,
                "question": "Approve this summary?",
                "status": "INTERRUPTED",
            }
        if not resumed_approval:
            return "Summary rejected by reviewer."
        return f"Approved and Published: {summary}"

    class StandaloneResearchRunner:
        def __init__(self) -> None:
            self.threads: Dict[str, str] = {}

        def invoke(self, arg: Any, config: Optional[Dict[str, Any]] = None) -> Any:
            thread_id = (config or {}).get("configurable", {}).get("thread_id", "demo-1")
            if isinstance(arg, Command):
                topic = self.threads.get(thread_id, "default topic")
                return standalone_agent_logic(topic, resumed_approval=arg.resume)
            self.threads[thread_id] = arg
            return standalone_agent_logic(arg)

    research_agent = StandaloneResearchRunner()


def main() -> None:
    """Run functional API workflow demonstrating pause and resume."""
    print("\n=== LangGraph Functional API Demo ===")
    print(f"Engine: {'LangGraph Native (@entrypoint/@task)' if HAS_LANGGRAPH_FUNC else 'Standalone Functional Runner'}\n")

    config = {"configurable": {"thread_id": "thread-2026-demo"}}
    test_topic = "Agentic AI in 2026"

    print(f"Step 1: Invoking entrypoint with topic: '{test_topic}'")
    interrupt_state = research_agent.invoke(test_topic, config=config)

    print("Step 2: Flow paused at interrupt point.")
    print(f"  Interrupt Payload: {interrupt_state}")
    assert "summary" in interrupt_state or "question" in interrupt_state

    print("\nStep 3: Resuming workflow with approval Command(resume=True)...")
    final_output = research_agent.invoke(Command(resume=True), config=config)
    print(f"  Final Resumed Output: {final_output}")
    assert "Approved and Published" in final_output

    print("\nFunctional API pause, interrupt, and resume verified successfully.")


if __name__ == "__main__":
    main()
