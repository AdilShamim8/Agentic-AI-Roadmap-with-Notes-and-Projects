"""A2A protocol from scratch, without the SDK.

Implements a minimal A2A v1.0 server as pure Python, to teach the wire
format from chapter 07/03 (updated to the current 1.0.0 revision):

- Agent Card served at /.well-known/agent-card.json
- JSON-RPC method `message/send` (v1.0 replaced the 0.2.x `tasks/send`)
- Task lifecycle: submitted -> working -> completed | failed | rejected
- The `rejected` terminal state added in v1.0

The handler is deterministic, so no API key is required. In production
you would use the `a2a-sdk` package (see chapter).

Run:
    python examples/a2a_from_scratch_demo.py
"""

from __future__ import annotations

from typing import Any

PROTOCOL_VERSION = "1.0.0"

AGENT_CARD: dict[str, Any] = {
    "name": "echo-research-agent",
    "description": "Echoes research tasks back with a citation plan.",
    "version": "1.0.0",
    "url": "http://localhost:8001",
    "capabilities": {"streaming": False, "pushNotifications": False},
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [
        {
            "id": "research",
            "name": "Research",
            "description": "Research a topic and return a cited summary.",
            "tags": ["research"],
        }
    ],
    "provider": {"organization": "agentic-ai-roadmap"},
}


class A2AFromScratchServer:
    """Minimal A2A v1.0 JSON-RPC dispatcher."""

    def __init__(self) -> None:
        self.tasks: dict[str, dict[str, Any]] = {}
        self._next_id = 0

    def handle_message(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        """Dispatch an A2A JSON-RPC request."""
        method = payload.get("method")
        req_id = payload.get("id")
        params: dict[str, Any] = payload.get("params") or {}

        if method == "message/send":
            return self._send_message(req_id, params)

        if method == "tasks/get":
            task_id = params.get("taskId")
            task = self.tasks.get(str(task_id))
            if task is None:
                return self._error(req_id, -32001, f"task {task_id!r} not found")
            return {"jsonrpc": "2.0", "id": req_id, "result": task}

        return self._error(req_id, -32601, f"method {method!r} not found")

    # -- handlers -------------------------------------------------------

    def _send_message(self, req_id: Any, params: dict[str, Any]) -> dict[str, Any]:
        message = params.get("message") or {}
        text = self._first_text(message)
        self._next_id += 1
        task_id = f"task-{self._next_id:03d}"

        if not text.strip():
            state = "rejected"  # terminal state added in A2A v1.0
            artifact = None
        else:
            state = "completed"
            artifact = {
                "parts": [{"kind": "text", "text": f"Echo: {text} (with citations)"}]
            }

        task = {
            "id": task_id,
            "contextId": params.get("configuration", {}).get("contextId", "ctx-1"),
            "status": {"state": state},
            "artifacts": [artifact] if artifact else [],
        }
        self.tasks[task_id] = task
        return {"jsonrpc": "2.0", "id": req_id, "result": task}

    @staticmethod
    def _first_text(message: dict[str, Any]) -> str:
        for part in message.get("parts", []):
            if part.get("kind") == "text":
                return str(part.get("text", ""))
        return ""

    @staticmethod
    def _error(req_id: Any, code: int, message: str) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def main() -> None:
    """Drive the v1.0 protocol end to end with a test client."""
    print("\n=== A2A from scratch demo (protocol v1.0.0) ===\n")
    server = A2AFromScratchServer()

    print("Agent Card well-known path: /.well-known/agent-card.json")
    print(f"Card skills: {[s['id'] for s in AGENT_CARD['skills']]}\n")

    # 1. message/send (the v1.0 name; 0.2.x used tasks/send)
    send = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": "Research agentic AI evaluation"}],
            }
        },
    }
    res = server.handle_message(send)
    assert res is not None
    task = res["result"]
    print(f"1. message/send -> task {task['id']} state={task['status']['state']}")
    assert task["status"]["state"] == "completed"
    assert task["artifacts"][0]["parts"][0]["text"].startswith("Echo:")

    # 2. tasks/get
    get = {"jsonrpc": "2.0", "id": 2, "method": "tasks/get",
           "params": {"taskId": task["id"]}}
    res2 = server.handle_message(get)
    assert res2 is not None
    print(f"2. tasks/get   -> task {res2['result']['id']} retrievable")

    # 3. Empty input must land in the v1.0 'rejected' terminal state
    bad = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "message/send",
        "params": {"message": {"role": "user", "parts": [{"kind": "text", "text": ""}]}},
    }
    res3 = server.handle_message(bad)
    assert res3 is not None
    print(f"3. empty input -> state={res3['result']['status']['state']} (v1.0 rejected)")
    assert res3["result"]["status"]["state"] == "rejected"

    # 4. Unknown task
    res4 = server.handle_message({"jsonrpc": "2.0", "id": 4,
                                  "method": "tasks/get", "params": {"taskId": "nope"}})
    assert res4 is not None
    print(f"4. tasks/get(missing) -> error {res4['error']['code']}")

    print("\nA2A v1.0 protocol checks passed.")


if __name__ == "__main__":
    main()
