"""MCP client demonstration with the real MultiServerMCPClient.

Demonstrates:
1. MultiServerMCPClient connecting to multiple MCP servers over stdio:
   the filesystem, web search, and SQLite servers from this repo.
2. Real tool discovery: tools/list from each server, converted into
   LangChain tools.
3. Dispatching tool calls to the right server.

This demo spawns the servers as subprocesses; no LLM and no API key are
required (tool calls only).

Run:
    python examples/mcp_client_demo.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import (
    SSEConnection,
    StdioConnection,
    StreamableHttpConnection,
    WebsocketConnection,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

# The constructor's parameter is the full connection union; annotate the
# manifest with it (dict is invariant, so a narrower dict type is rejected).
Connection = (
    StdioConnection | SSEConnection | StreamableHttpConnection | WebsocketConnection
)

SERVER_MANIFEST: dict[str, Connection] = {
    "filesystem": {
        "command": sys.executable,
        "args": [str(REPO_ROOT / "examples" / "mcp_filesystem_server.py")],
        "transport": "stdio",
    },
    "web_search": {
        "command": sys.executable,
        "args": [str(REPO_ROOT / "examples" / "mcp_websearch_server.py")],
        "transport": "stdio",
    },
    "sqlite": {
        "command": sys.executable,
        "args": [str(REPO_ROOT / "examples" / "mcp_sqlite_server.py")],
        "transport": "stdio",
    },
}


async def run_mcp_client_workflow() -> None:
    """Connect, discover tools, and dispatch calls across servers."""
    print("\n=== Multi-server MCP client demo ===")
    client = MultiServerMCPClient(SERVER_MANIFEST)
    tools = await client.get_tools()
    print(f"Connected to {len(SERVER_MANIFEST)} servers; "
          f"discovered {len(tools)} tools:")
    by_name = {t.name: t for t in tools}
    for t in tools:
        print(f"  - {t.name}: {t.description.splitlines()[0][:70]}")

    for expected in ("read_file", "list_directory", "web_search", "query_database"):
        assert expected in by_name, f"missing tool: {expected}"

    print("\nDispatching tool calls across servers:")

    # 1. Filesystem: read a real file through the MCP server.
    result = await by_name["read_file"].ainvoke(
        {"path": str(REPO_ROOT / "README.md")}
    )
    text = str(result)
    print(f"  1. read_file(README.md) -> {text[:60]!r}...")
    assert "Agentic AI Roadmap" in text

    # 2. Web search: the curated search index inside the server.
    result = await by_name["web_search"].ainvoke(
        {"query": "Model Context Protocol LangGraph"}
    )
    print(f"  2. web_search(...) -> {str(result)[:60]!r}...")
    assert "modelcontextprotocol.io" in str(result)

    # 3. SQLite: query the demo database inside the server.
    result = await by_name["query_database"].ainvoke(
        {"sql": "SELECT name, provider FROM models LIMIT 3"}
    )
    print(f"  3. query_database(...) -> {str(result)[:60]!r}...")

    print("\nAll multi-server discovery and dispatch checks passed.")


def main() -> None:
    """Run the client workflow."""
    asyncio.run(run_mcp_client_workflow())


if __name__ == "__main__":
    main()
