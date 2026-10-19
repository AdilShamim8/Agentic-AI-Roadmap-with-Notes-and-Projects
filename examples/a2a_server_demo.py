"""Expose a LangGraph agent as an A2A v1.0 server.

Implements chapter 07/04 against the current protocol revision (1.0.0):
- Agent Card at /.well-known/agent-card.json (the v1.0 path; 0.2.x used
  agent.json)
- JSON-RPC `message/send` over HTTP POST
- Task lifecycle incl. the `rejected` state

The served agent is a LangGraph StateGraph with mocked content, so the
demo runs without an API key. In production you would use the
`a2a-sdk` server stack (see chapter).

Run:
    python examples/a2a_server_demo.py

Requires the deploy extra (fastapi):
    pip install -e ".[deploy]"

Serve (in one terminal):
    uvicorn examples.a2a_server_demo:app --port 8001
"""

from __future__ import annotations

from typing import Any, TypedDict

import httpx
from fastapi import FastAPI
from langgraph.graph import END, START, StateGraph

APP_NAME = "research-agent"


class ResearchState(TypedDict):
    topic: str
    summary: str


def synthesize(state: ResearchState) -> dict:
    """The research agent's node (mocked content; an LLM in production)."""
    return {"summary": f"Cited summary of {state['topic']!r} (mocked)"}


def build_research_agent():
    workflow = StateGraph(ResearchState)
    workflow.add_node("synthesize", synthesize)
    workflow.add_edge(START, "synthesize")
    workflow.add_edge("synthesize", END)
    return workflow.compile()


research_agent = build_research_agent()

AGENT_CARD: dict[str, Any] = {
    "name": APP_NAME,
    "description": "Researches a topic and returns a cited summary.",
    "version": "1.0.0",
    "url": "http://localhost:8001",
    "capabilities": {"streaming": False, "pushNotifications": False},
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [
        {
            "id": "research",
            "name": "Research",
            "description": "Research a topic and return a summary with citations.",
            "tags": ["research"],
        }
    ],
    "provider": {"organization": "agentic-ai-roadmap"},
}

_tasks: dict[str, dict[str, Any]] = {}
_next_id = 0

app = FastAPI(title=APP_NAME)


@app.get("/.well-known/agent-card.json")
def agent_card() -> dict[str, Any]:
    """Serve the Agent Card at the v1.0 well-known path."""
    return AGENT_CARD


@app.post("/")
def message_send(payload: dict[str, Any]) -> dict[str, Any]:
    """Handle a JSON-RPC `message/send` (v1.0) request."""
    global _next_id
    method = payload.get("method")
    if method != "message/send":
        return {"jsonrpc": "2.0", "id": payload.get("id"),
                "error": {"code": -32601, "message": f"method {method!r} not supported"}}

    params: dict[str, Any] = payload.get("params") or {}
    message = params.get("message") or {}
    text = next(
        (str(p.get("text", "")) for p in message.get("parts", [])
         if p.get("kind") == "text"),
        "",
    )

    if not text.strip():
        state = "rejected"  # v1.0 terminal state for unusable input
        artifacts = []
    else:
        result = research_agent.invoke({"topic": text, "summary": ""})
        state = "completed"
        artifacts = [{"parts": [{"kind": "text", "text": result["summary"]}]}]

    _next_id += 1
    task_id = f"task-{_next_id:03d}"
    task = {
        "id": task_id,
        "contextId": "ctx-1",
        "status": {"state": state},
        "artifacts": artifacts,
    }
    _tasks[task_id] = task
    return {"jsonrpc": "2.0", "id": payload.get("id"), "result": task}


@app.get("/tasks/{task_id}")
def get_task(task_id: str) -> dict[str, Any]:
    """Retrieve a task by id."""
    task = _tasks.get(task_id)
    if task is None:
        return {"error": {"code": -32001, "message": f"task {task_id!r} not found"}}
    return task


async def run_client_demo() -> None:
    """Exercise the server in-process via an ASGI transport."""
    print("\n=== A2A server demo (protocol v1.0.0) ===\n")
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        card = (await client.get("/.well-known/agent-card.json")).json()
        print(f"1. fetched Agent Card: {card['name']} (v{card['version']})")
        assert card["name"] == APP_NAME

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"kind": "text", "text": "agentic AI evaluation"}],
                }
            },
        }
        resp = (await client.post("/", json=payload)).json()
        task = resp["result"]
        print(f"2. message/send -> task {task['id']} state={task['status']['state']}")
        assert task["status"]["state"] == "completed"
        assert "Cited summary" in task["artifacts"][0]["parts"][0]["text"]

        fetched = (await client.get(f"/tasks/{task['id']}")).json()
        print(f"3. tasks/get   -> {fetched['status']['state']}")

        bad = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "message/send",
            "params": {"message": {"role": "user",
                                   "parts": [{"kind": "text", "text": "   "}]}},
        }
        bad_resp = (await client.post("/", json=bad)).json()
        print(f"4. blank input -> state={bad_resp['result']['status']['state']}")
        assert bad_resp["result"]["status"]["state"] == "rejected"

    print("\nA2A v1.0 server checks passed.")


def main() -> None:
    """Run the in-process client demo."""
    import asyncio

    asyncio.run(run_client_demo())


if __name__ == "__main__":
    main()
