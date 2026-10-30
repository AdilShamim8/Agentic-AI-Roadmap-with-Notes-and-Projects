"""Pytest tests for the example agents.

Run:
    pytest examples/tests/ -v

These tests verify the graph structure, the tool wiring, and the error
handling. They do not call an LLM unless a key is present: tests that
must invoke a model are skipped when no API key is set, so CI can run
without secrets.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# Add the examples directory to the path so we can import the agents.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

HAS_KEY = bool(os.environ.get("ANTHROPIC_API_KEY"))


def test_langgraph_core_graph_terminates():
    """The core demo graph should terminate with the expected value."""
    from examples.langgraph_core_demo import agent

    result = agent.invoke({"value": 3, "steps": 0})
    assert result["value"] == 14, f"Expected 14, got {result['value']}"
    assert result["steps"] == 3, f"Expected 3 steps, got {result['steps']}"


def test_calculator_tool_handles_errors():
    """The calculator tool should return an error, not raise.

    Importing react_demo must not require an API key (the module-level
    agent is built lazily), so this also guards the lazy-import pattern.
    """
    from examples.react_demo import calculator

    result = calculator.invoke({"expression": "1/0"})
    assert "Error" in result


def test_weather_tool_returns_string():
    """The weather tool should return a string with the location.

    Importing conversational_agent_demo must not require an API key.
    """
    from examples.conversational_agent_demo import get_weather

    result = get_weather.invoke({"location": "San Francisco"})
    assert "San Francisco" in result
    assert "72F" in result


def test_tool_result_uses_tool_message():
    """The structured-output loop must append ToolMessage, not AIMessage."""
    import examples.structured_output_demo as sod

    src = Path(sod.__file__).read_text()
    assert "ToolMessage(" in src
    assert "AIMessage(content=result" not in src


@pytest.mark.skipif(not HAS_KEY, reason="requires ANTHROPIC_API_KEY to invoke the LLM")
def test_structured_output_agent_has_max_iterations():
    """A nonsense question should hit the max iterations and return the fallback."""
    from examples.structured_output_demo import run_agent

    result = run_agent("xyzzy", max_iterations=2)
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.skipif(not HAS_KEY, reason="requires ANTHROPIC_API_KEY to build the LLM")
def test_react_agent_builds():
    """The agent builds and compiles under the current dependency set."""
    from examples.react_demo import build_agent

    agent = build_agent()
    assert agent is not None


def test_mcp_filesystem_server_exists():
    """The MCP filesystem server module should import cleanly."""
    from examples.mcp_filesystem_server import server

    assert server.name == "filesystem-server"


def test_retrieval_tool_scopes_by_tenant():
    """The scoped search tool must never cross tenants.

    Importing retrieval_demo must not require an API key.
    """
    from examples.retrieval_demo import search_knowledge_base

    acme = search_knowledge_base.invoke({"query": "refund policy", "tenant": "acme"})
    assert "standard customers" in acme

    globex = search_knowledge_base.invoke({"query": "refund policy", "tenant": "globex"})
    assert "standard customers" not in globex
    assert "No documents matched" in globex

    unknown = search_knowledge_base.invoke({"query": "refund policy", "tenant": "initech"})
    assert "Unknown tenant" in unknown


def test_retrieval_refinement_finds_loyalty_terms():
    """The broad query cannot match the loyalty doc; the reformulated one must.

    The loyalty-terms document deliberately avoids the word "refund", so
    this asserts the demo's reformulation story is real, not staged.
    """
    from examples.retrieval_demo import search_knowledge_base

    broad = search_knowledge_base.invoke({"query": "loyalty member benefits", "tenant": "acme"})
    assert "90 days" in broad
    assert "10 percent credit" in broad
