# A2A agent cards

Module: 07-multi-agent-and-a2a
Chapter: 04-a2a-agent-cards
Status: beta
Last reviewed: 2026-10-19
Estimated time: 2 hours

## Learning objectives

- Author an Agent Card that accurately advertises an agent's capabilities
- Expose a LangGraph agent as an A2A server
- Consume an A2A agent from a LangGraph client
- Use the A2A registry for discovery

## Prerequisites

- [03 A2A protocol](03-a2a-protocol.md)

## Conceptual foundation

The Agent Card is the public face of an A2A agent. It is a JSON document at `/.well-known/agent-card.json` (the v1.0 path; 0.2.x used `agent.json`) that tells potential clients: who I am, what I can do, how to call me, what authentication I require. v1.0 adds signed cards (AgentCardSignature) so callers can verify a card was not tampered with, and an authenticated "extended card" for callers you already trust. A well-authored Agent Card is the difference between an agent that gets used and one that does not.

The v1.0 required fields:

- `name`: the agent's name (e.g., "research-agent").
- `description`: a one-paragraph description of what the agent does. This is what clients read to decide whether to use the agent.
- `url`: the service URL where the agent receives requests (the card carries one URL, not a list of endpoints).
- `version`: the agent's version (semantic versioning).
- `capabilities`: what the agent supports (streaming, push notifications).
- `defaultInputModes` / `defaultOutputModes`: the MIME types the agent accepts and produces.
- `skills`: a list of skills the agent has. Each skill has an id, a name, a description, and tags.
- `securitySchemes`: the authentication schemes (API key, OAuth, mutual TLS), mirroring OpenAPI's structure.

The `skills` field is the most important. It is the agent's menu. Each skill should be specific enough that a client can decide whether the agent can handle a given task. "Research" is too vague; "Research a topic using web search and return a cited summary" is specific.

## Worked example

Exposing a LangGraph research agent as an A2A v1.0 server. Full code (FastAPI, in-process client tests, the `rejected` state) in [`examples/a2a_server_demo.py`](../examples/a2a_server_demo.py).

```python
from fastapi import FastAPI
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

app = FastAPI()

@tool
def web_search(query: str) -> str:
    """Search the web."""
    return f"[Results for: {query}]"

llm = ChatAnthropic(model="claude-sonnet-5-5")
research_agent = create_react_agent(llm, tools=[web_search], prompt="You are a research agent.")

AGENT_CARD = {
    "name": "research-agent",
    "description": "Researches a topic and returns a cited summary.",
    "version": "1.0.0",
    "url": "http://localhost:8001",
    "capabilities": {"streaming": False, "pushNotifications": False},
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [{
        "id": "research", "name": "Research",
        "description": "Research a topic and return a summary with citations.",
        "tags": ["research"],
    }],
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
        state, artifacts = "rejected", []  # v1.0 terminal state
    else:
        result = research_agent.invoke(
            {"messages": [{"role": "user", "content": f"Research: {text}"}]}
        )
        state = "completed"
        artifacts = [{"parts": [{"kind": "text", "text": result["messages"][-1].content}]}]
    return {"jsonrpc": "2.0", "id": payload["id"], "result": {
        "id": "task-001", "contextId": "ctx-1",
        "status": {"state": state}, "artifacts": artifacts,
    }}
```

Consuming the agent from a client:

```python
import httpx
from langchain_core.tools import tool

@tool
def call_research_agent(topic: str) -> str:
    """Research a topic using the remote research agent. Returns a summary."""
    # 1. Fetch the Agent Card (cached in production)
    card = httpx.get("http://localhost:8001/.well-known/agent-card.json").json()

    # 2. Send a message (v1.0 method name; 0.2.x used tasks/send)
    response = httpx.post(card["url"], json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {"message": {"role": "user", "parts": [{"kind": "text", "text": topic}]}},
    }, headers={"Authorization": "Bearer ..."})

    task = response.json()["result"]
    return task["artifacts"][0]["parts"][0]["text"]
```

## Evaluation

Test that: (1) the Agent Card is served correctly, (2) a client can discover the agent and send a task, (3) the agent returns a valid artifact, (4) the client can use the agent as a tool in a larger graph.

## Production notes

In production, A2A servers are deployed like any HTTP service: behind a load balancer, with authentication, with rate limiting, with observability. The Agent Card is cached by clients (it does not change often). The task lifecycle is asynchronous for long-running tasks (the client polls or receives a webhook). Authentication is typically bearer token or OAuth.

## Common pitfalls

- Vague skill descriptions. Why: the author knows what the agent does. Fix: write specific skill descriptions; they are how clients decide.
- Not serving the Agent Card at the well-known URL. Why: it works when the URL is known. Fix: use `/.well-known/agent-card.json`.
- Synchronous-only for long tasks. Why: it works in dev. Fix: use async mode.

## Further reading

- [A2A protocol specification](https://a2a-protocol.org/latest/specification/)
- [A2A Agent Card reference](https://a2a-protocol.org/latest/specification/)

## Checklist

- [ ] Author an Agent Card with specific skill descriptions
- [ ] Expose a LangGraph agent as an A2A v1.0 server
- [ ] Consume an A2A agent from a client as a tool
- [ ] Use async mode for long-running tasks

