"""Model Context Protocol (MCP) from scratch without external frameworks.

Demonstrates the core JSON-RPC 2.0 protocol mechanics:
1. 'initialize' handshake with protocolVersion negotiation and capabilities
2. 'tools/list' schema discovery and validation
3. 'tools/call' execution and formatted content response
4. JSON-RPC error handling for non-existent tools and malformed payloads

Run:
    python examples/mcp_from_scratch_demo.py
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional


class MCPFromScratchServer:
    """Pure-Python implementation of an MCP server adhering to JSON-RPC 2.0."""

    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self, name: str = "demo-scratch-server", version: str = "1.0.0") -> None:
        self.name = name
        self.version = version

    def handle_message(self, request_payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process an incoming JSON-RPC 2.0 request or notification."""
        jsonrpc = request_payload.get("jsonrpc")
        method = request_payload.get("method")
        req_id = request_payload.get("id")
        params = request_payload.get("params", {})

        # Validation of basic JSON-RPC 2.0 envelope
        if jsonrpc != "2.0":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": "Invalid Request: jsonrpc must be '2.0'"},
            }

        # Handle handshake
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": self.PROTOCOL_VERSION,
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": self.name, "version": self.version},
                },
            }

        # Notifications (no id, no response expected)
        if method == "notifications/initialized":
            return None

        # Tool discovery
        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "echo",
                            "description": "Echoes the input back to verify transport integrity.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"text": {"type": "string", "description": "Text to echo."}},
                                "required": ["text"],
                            },
                        },
                        {
                            "name": "add",
                            "description": "Adds two numbers together deterministically.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "a": {"type": "number", "description": "First addend."},
                                    "b": {"type": "number", "description": "Second addend."},
                                },
                                "required": ["a", "b"],
                            },
                        },
                    ]
                },
            }

        # Tool execution
        if method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name == "echo":
                text = args.get("text", "")
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Echo: {text}"}],
                        "isError": False,
                    },
                }

            if tool_name == "add":
                a = args.get("a", 0)
                b = args.get("b", 0)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": str(a + b)}],
                        "isError": False,
                    },
                }

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: Tool '{tool_name}' does not exist."},
            }

        # Unknown RPC method
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Procedure '{method}' not recognized."},
        }


def main() -> None:
    """Test full MCP handshake, tool discovery, and execution cycle."""
    print("\n=== Model Context Protocol (MCP) From Scratch Demo ===")
    server = MCPFromScratchServer()

    # Step 1: Handshake
    print("Step 1: Client sends 'initialize' request...")
    init_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0"},
        },
    }
    init_res = server.handle_message(init_req)
    print(f"  Handshake Response: {json.dumps(init_res, indent=2)}")
    assert init_res["result"]["serverInfo"]["name"] == "demo-scratch-server"

    # Step 2: Tool Discovery
    print("\nStep 2: Client sends 'tools/list' request...")
    list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    list_res = server.handle_message(list_req)
    tools = list_res["result"]["tools"]
    print(f"  Discovered {len(tools)} tools: {[t['name'] for t in tools]}")
    assert len(tools) == 2

    # Step 3: Tool Execution ('echo')
    print("\nStep 3: Client calls 'echo' tool...")
    call_req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "echo", "arguments": {"text": "Agentic AI 2026"}},
    }
    call_res = server.handle_message(call_req)
    print(f"  Execution Response: {call_res['result']['content'][0]['text']}")
    assert call_res["result"]["content"][0]["text"] == "Echo: Agentic AI 2026"

    # Step 4: Tool Execution ('add')
    print("\nStep 4: Client calls 'add' tool...")
    add_req = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {"name": "add", "arguments": {"a": 40, "b": 2}},
    }
    add_res = server.handle_message(add_req)
    print(f"  Result: 40 + 2 = {add_res['result']['content'][0]['text']}")
    assert add_res["result"]["content"][0]["text"] == "42"

    # Step 5: Error handling on non-existent tool
    print("\nStep 5: Testing error handling on unknown tool...")
    err_req = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {"name": "non_existent_tool", "arguments": {}},
    }
    err_res = server.handle_message(err_req)
    print(f"  RPC Error code: {err_res['error']['code']}, message: {err_res['error']['message']}")
    assert err_res["error"]["code"] == -32601

    print("\nAll MCP JSON-RPC protocol tests passed successfully.")


if __name__ == "__main__":
    main()
