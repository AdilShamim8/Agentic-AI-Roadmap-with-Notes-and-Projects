# A2A protocol

Module: 07-multi-agent-and-a2a
Chapter: 03-a2a-protocol
Status: beta
Last reviewed: 2026-10-19
Estimated time: 3 hours

## Learning objectives

- Explain the A2A protocol (Agent-to-Agent, announced by Google in 2025)
- Describe the Agent Card (the JSON manifest that advertises an agent's capabilities)
- Describe the task lifecycle (submitted, working, input-required, completed, failed)
- Build a minimal A2A server and client by hand (without the SDK) to understand the protocol

## Prerequisites

- [02 Agent handoffs](02-agent-handoffs.md)

## Conceptual foundation

The Agent-to-Agent (A2A) protocol is to agents what MCP is to tools: an open protocol that decouples agent authoring from agent framework. A2A was announced by Google in April 2025, reached v1.0.0 in 2026, and is now stewarded by the Agentic AI Foundation with SDKs in Python, Go, Java, JS, .NET, and Rust. The promise: an agent built with LangGraph can call an agent built with OpenAI's Agents SDK, which can call an agent built with CrewAI, all speaking the same protocol.

The protocol is HTTP-based, with JSON payloads. v1.0.0 defines one canonical data model bound to three interchangeable transports (JSON-RPC, gRPC, HTTP/REST) that must behave identically. The core concepts:

1. Agent Card. A JSON document hosted at a well-known URL - `/.well-known/agent-card.json` in v1.0 (0.2.x used `agent.json`) - that advertises the agent's identity, capabilities, skills, service URL, and security schemes. The Agent Card is how agents discover each other, and v1.0 adds signed cards and an authenticated "extended card" for callers you trust.

2. Task. The unit of work in A2A. A client sends a message; the agent returns a task that tracks the work. Tasks have a lifecycle: `submitted` (received), `working` (in progress), `input-required` (agent needs more input from the client), `completed` (done), `failed` (error), `canceled` (client canceled), `rejected` (v1.0 terminal state for unusable input). Multi-turn conversations are tied together with a `contextId`.

3. Message. A message in a task, from either the client or the agent. Messages have a role (`user` or `agent`) and a list of parts (text, file, data).

4. Part. A piece of a message. Text parts are the most common; file parts carry binary data; data parts carry structured JSON.

5. Artifact. The output of a task. A task can produce multiple artifacts (e.g., a report text and a chart image).

The lifecycle of a typical A2A interaction (v1.0 method names - `message/send` replaced the 0.2.x `tasks/send`):

1. The client fetches the agent's Agent Card from `/.well-known/agent-card.json`.
2. The client sends a `message/send` request (or `message/stream` for streaming) with the message.
3. The agent starts working and returns a task in `working` status.
4. (Optional) The agent sends an `input-required` status, asking for clarification. The client responds with another `message/send` on the same `contextId`.
5. The agent completes and returns a `completed` status with artifacts. The client can also `tasks/get`, `tasks/list`, or `tasks/cancel`.

A2A supports both synchronous (the request blocks until the task completes) and asynchronous (the request returns immediately, the client polls or receives webhooks) modes. For long-running tasks, asynchronous is required.

Why A2A matters: it is the interop layer that makes multi-framework agent systems possible. Without A2A, an agent built with framework X can only call agents built with framework X. With A2A, an agent built with any framework can call agents built with any other framework. This is the same decoupling that HTTP achieved for web services, and it will have the same effect on the agent ecosystem.

## Worked example

A minimal A2A v1.0 server and client, without the SDK, to show the wire format. The runnable version (including the v1.0 `rejected` state) is in [`examples/a2a_from_scratch_demo.py`](../examples/a2a_from_scratch_demo.py).

```python
# Server (FastAPI)
from fastapi import FastAPI

app = FastAPI()

AGENT_CARD = {
    "name": "echo-agent",
    "description": "Echoes the input back. Useful for testing.",
    "version": "1.0.0",
    "url": "http://localhost:8001",
    "capabilities": {"streaming": False, "pushNotifications": False},
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [{"id": "echo", "name": "Echo", "description": "Echoes the input.", "tags": ["test"]}],
    "provider": {"organization": "agentic-ai-roadmap"},
}

@app.get("/.well-known/agent-card.json")
def agent_card():
    return AGENT_CARD

@app.post("/")
def message_send(payload: dict):
    text = next(
        (p.get("text", "") for p in payload["params"]["message"]["parts"]
         if p.get("kind") == "text"), "",
    )
    if not text.strip():
        state = "rejected"  # v1.0 terminal state for unusable input
        artifacts = []
    else:
        state = "completed"
        artifacts = [{"parts": [{"kind": "text", "text": f"Echo: {text}"}]}]
    return {"jsonrpc": "2.0", "id": payload["id"], "result": {
        "id": "task-001", "contextId": "ctx-1",
        "status": {"state": state}, "artifacts": artifacts,
    }}

# Client (httpx)
import httpx

def call_a2a_agent(base_url: str, message: str):
    card = httpx.get(f"{base_url}/.well-known/agent-card.json").json()
    print(f"Agent: {card['name']} - {card['description']}")

    response = httpx.post(f"{base_url}/", json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",  # v1.0; 0.2.x used tasks/send
        "params": {"message": {"role": "user", "parts": [{"kind": "text", "text": message}]}},
    })
    task = response.json()["result"]
    print(f"State: {task['status']['state']}")
    if task["artifacts"]:
        print(f"Artifact: {task['artifacts'][0]['parts'][0]['text']}")
```

In production, you would use the A2A SDK (`a2a-sdk` on PyPI, repo [a2aproject/a2a-python](https://github.com/a2aproject/a2a-python)), which handles the protocol plumbing, authentication, streaming, and push notifications.

## Evaluation

Test the server by: (1) fetching the Agent Card, (2) sending a task, (3) verifying the artifact. The eval is a set of HTTP fixtures.

## Production notes

In production, A2A servers are typically deployed as HTTP services (behind a load balancer, with authentication, with rate limiting). The Agent Card is served at a well-known URL. The client discovers the agent, sends tasks, and receives artifacts. The same patterns as any HTTP API apply: authentication, rate limiting, observability, versioning.

The main production risk: A2A is new (2025-2026), and the spec is evolving. Pin the protocol version your server and client use. Do not assume the spec is stable yet.

## Common pitfalls

- Confusing A2A with MCP. Why: they sound similar. Fix: MCP is for tools (functions); A2A is for agents (which may use tools).
- Not serving the Agent Card at the well-known URL. Why: it works when the client knows the URL. Fix: use `/.well-known/agent-card.json`; that is how discovery works.
- Synchronous-only for long-running tasks. Why: it works in dev. Fix: use async mode for tasks that take more than a few seconds.

## Further reading

- [A2A protocol specification](https://a2a-protocol.org/latest/specification/)
- [a2aproject/A2A on GitHub](https://github.com/a2aproject/A2A)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python)

## Checklist

- [ ] Explain the A2A protocol and how it differs from MCP
- [ ] Describe the v1.0 Agent Card path, the task lifecycle (including `rejected`), and the `message/send` method
- [ ] Build a minimal A2A server and client by hand
- [ ] Discover an agent by fetching its Agent Card
