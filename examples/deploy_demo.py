"""Deployment demonstration: the langgraph.json contract.

Implements chapter 08/01's self-hosted path with the current CLI flow
(`langgraph dev` for development, `langgraph build` + `langgraph up`
for self-hosted deployment; the old prebuilt `langchain/langgraph` base
image no longer exists). This demo validates the deployment contract:

1. `langgraph.json` points at a real, importable graph
2. The graph compiles and answers a smoke request
3. The required commands are printed for the reader

Runs without an API key (deterministic agent).

Run:
    python examples/deploy_demo.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

REPO_ROOT = Path(__file__).resolve().parent.parent
LANGGRAPH_JSON = REPO_ROOT / "08-production" / "langgraph.json"


class DeployState(TypedDict):
    question: str
    answer: str


def respond(state: DeployState) -> dict:
    """The deployed agent's node (mocked content; an LLM in production)."""
    return {"answer": f"deployed answer to {state['question']!r} (mocked)"}


def build_deployed_agent():
    """Build the graph that langgraph.json exposes."""
    workflow = StateGraph(DeployState)
    workflow.add_node("respond", respond)
    workflow.add_edge(START, "respond")
    workflow.add_edge("respond", END)
    return workflow.compile()


# The module-level graph referenced by langgraph.json.
agent = build_deployed_agent()


def validate_langgraph_json() -> dict:
    """The deployment contract: langgraph.json must point at a real graph."""
    config = json.loads(LANGGRAPH_JSON.read_text())
    graphs = config.get("graphs", {})
    assert graphs, "langgraph.json exposes no graphs"
    for name, ref in graphs.items():
        module_path, _, attr = ref.partition(":")
        assert attr, f"graph {name!r} reference must be 'module:attribute'"
        module_path = module_path.lstrip("./").removesuffix(".py")
        module = __import__(module_path.replace("/", "."), fromlist=["x"])
        compiled = getattr(module, attr, None)
        assert compiled is not None, f"graph {name!r}: {ref} resolved to nothing"
        assert hasattr(compiled, "invoke"), f"graph {name!r} is not compiled"
    return config


def main() -> None:
    """Validate the contract, run a smoke request, print the commands."""
    print("\n=== Deploy demo ===\n")

    config = validate_langgraph_json()
    print(f"langgraph.json graphs: {list(config['graphs'])} - all import and compile")

    result = agent.invoke({"question": "smoke test", "answer": ""})
    print(f"Smoke request -> {result['answer']}")

    print("\nCommands (current CLI):")
    print("  development:      langgraph dev        # hot-reload dev server")
    print("  build an image:   langgraph build      # container image for self-hosting")
    print("  self-host:        langgraph up         # runs the built image")
    print("  managed:          langgraph deploy     # LangSmith Deployment")
    print("\nDeployment contract checks passed.")


if __name__ == "__main__":
    main()
