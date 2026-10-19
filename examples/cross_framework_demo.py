"""Cross-framework interop demonstration over A2A v1.0.

Implements chapter 07/05: a LangGraph supervisor delegates to two remote
agents served over A2A - one written in the style of the OpenAI Agents
SDK, one in the style of a CrewAI crew. The frameworks never share code;
they interoperate purely through the protocol.

The remote agents are mocked stand-ins served in-process (ASGI), so the
demo runs without any API key. Swap the agent bodies for real OpenAI
Agents SDK / CrewAI code in production (see chapter).

Run:
    python examples/cross_framework_demo.py

Requires the deploy extra (fastapi):
    pip install -e ".[deploy]"
"""

from __future__ import annotations

import asyncio
from typing import Any

import httpx
from fastapi import FastAPI

# --- Remote agent 1: "OpenAI Agents SDK style" --------------------------

coder_app = FastAPI(title="coder-agent")
coder_card: dict[str, Any] = {
    "name": "coder-agent",
    "description": "Writes code changes. OpenAI Agents SDK style.",
    "version": "1.0.0",
    "url": "http://test/coder",
    "capabilities": {"streaming": False, "pushNotifications": False},
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [{"id": "code", "name": "Code",
                "description": "Produce a code change for a task.",
                "tags": ["coding"]}],
    "provider": {"organization": "agentic-ai-roadmap"},
}


@coder_app.get("/.well-known/agent-card.json")
def coder_card_endpoint() -> dict[str, Any]:
    return coder_card


@coder_app.post("/")
def coder_send(payload: dict[str, Any]) -> dict[str, Any]:
    text = next(
        (str(p.get("text", "")) for p in
         (payload.get("params") or {}).get("message", {}).get("parts", [])
         if p.get("kind") == "text"),
        "",
    )
    return {
        "jsonrpc": "2.0",
        "id": payload.get("id"),
        "result": {
            "id": "coder-task-1",
            "contextId": "ctx-coder",
            "status": {"state": "completed"},
            "artifacts": [{"parts": [{"kind": "text",
                                      "text": f"[coder] patch for {text!r} (mocked)"}]}],
        },
    }


# --- Remote agent 2: "CrewAI style" -------------------------------------

crew_app = FastAPI(title="research-crew")
crew_card: dict[str, Any] = {
    "name": "research-crew",
    "description": "Researches topics. CrewAI style.",
    "version": "1.0.0",
    "url": "http://test/crew",
    "capabilities": {"streaming": False, "pushNotifications": False},
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [{"id": "research", "name": "Research",
                "description": "Research a topic and return findings.",
                "tags": ["research"]}],
    "provider": {"organization": "agentic-ai-roadmap"},
}


@crew_app.get("/.well-known/agent-card.json")
def crew_card_endpoint() -> dict[str, Any]:
    return crew_card


@crew_app.post("/")
def crew_send(payload: dict[str, Any]) -> dict[str, Any]:
    text = next(
        (str(p.get("text", "")) for p in
         (payload.get("params") or {}).get("message", {}).get("parts", [])
         if p.get("kind") == "text"),
        "",
    )
    return {
        "jsonrpc": "2.0",
        "id": payload.get("id"),
        "result": {
            "id": "crew-task-1",
            "contextId": "ctx-crew",
            "status": {"state": "completed"},
            "artifacts": [{"parts": [{"kind": "text",
                                      "text": f"[crew] findings on {text!r} (mocked)"}]}],
        },
    }


# --- LangGraph supervisor consuming both over A2A -----------------------


async def call_a2a(client: httpx.AsyncClient, path: str, task: str) -> str:
    """A2A client tool: fetch the card, then message/send."""
    card = (await client.get(f"{path}/.well-known/agent-card.json")).json()
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {"message": {"role": "user",
                               "parts": [{"kind": "text", "text": task}]}},
    }
    resp = (await client.post(f"{path}/", json=payload)).json()
    task_obj = resp["result"]
    assert task_obj["status"]["state"] == "completed", f"{card['name']} failed"
    return task_obj["artifacts"][0]["parts"][0]["text"]


async def run_demo() -> None:
    print("\n=== Cross-framework interop demo (A2A v1.0) ===\n")
    # Two apps need two mounts; use a tiny router app for the demo.
    root = FastAPI()
    root.mount("/coder", coder_app)
    root.mount("/crew", crew_app)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=root),
                                 base_url="http://test") as client:
        coder_result = await call_a2a(client, "/coder",
                                      "add a rate limiter to the API")
        print(f"1. coder agent replied: {coder_result}")
        assert "[coder]" in coder_result

        crew_result = await call_a2a(client, "/crew",
                                     "rate limiting strategies")
        print(f"2. research crew replied: {crew_result}")
        assert "[crew]" in crew_result

    print("\nBoth frameworks interop over A2A v1.0. Supervisor checks passed.")


def main() -> None:
    asyncio.run(run_demo())


if __name__ == "__main__":
    main()
