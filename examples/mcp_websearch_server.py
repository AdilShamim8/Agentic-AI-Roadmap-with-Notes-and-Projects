"""MCP web search server.

Exposes tools over the Model Context Protocol for web search:
- web_search: retrieves curated search results with snippets, URLs, titles

The search index is a small curated list (deterministic, no API key);
in production, swap the handler body for Tavily, Brave, or another API.

Run:
    python examples/mcp_websearch_server.py

With a terminal stdin (no MCP client attached) this runs a self-test;
with a piped stdin (an MCP client spawned us) it speaks JSON-RPC.
"""

from __future__ import annotations

import sys
from typing import Any

import anyio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

server = Server("websearch-server")

# Curated reference index for deterministic evaluation and testing.
KNOWLEDGE_INDEX: list[dict[str, Any]] = [
    {
        "title": "Model Context Protocol (MCP)",
        "url": "https://modelcontextprotocol.io",
        "snippet": (
            "An open standard for connecting AI assistants to data "
            "sources, tools, and development environments."
        ),
        "keywords": ["mcp", "model context protocol", "tools", "specification"],
    },
    {
        "title": "LangGraph",
        "url": "https://docs.langchain.com/langgraph",
        "snippet": (
            "A library for building stateful, multi-actor applications "
            "with LLMs: cycles, persistence, and human-in-the-loop."
        ),
        "keywords": ["langgraph", "agents", "state", "orchestration", "multi-agent"],
    },
    {
        "title": "Agent2Agent (A2A) Protocol",
        "url": "https://a2a-protocol.org",
        "snippet": (
            "An open standard for agent-to-agent interoperability: "
            "discovery, task lifecycle, and cross-framework handoffs."
        ),
        "keywords": ["a2a", "handoff", "interop", "multi-agent"],
    },
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List the tools this server exposes."""
    return [
        Tool(
            name="web_search",
            description=(
                "Search the web for technical documentation, research "
                "papers, and developer ecosystem guides. Returns titles, "
                "URLs, and text snippets."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query keywords",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 3)",
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute web search operations safely and return text content."""
    try:
        if name == "web_search":
            query = arguments.get("query", "").lower()
            limit = int(arguments.get("limit", 3))

            if not query.strip():
                return [
                    TextContent(
                        type="text",
                        text="Search error: query string cannot be empty.",
                    )
                ]

            query_terms = query.split()
            matched = []
            for item in KNOWLEDGE_INDEX:
                title = item["title"].lower()
                kws = [k.lower() for k in item["keywords"]]
                score = sum(
                    1 for term in query_terms if term in title or term in kws
                )
                if score > 0:
                    matched.append((score, item))

            matched.sort(key=lambda pair: pair[0], reverse=True)
            results = [item for _, item in matched[:limit]]
            if not results:
                results = KNOWLEDGE_INDEX[:limit]

            formatted = "\n\n".join(
                f"[{idx + 1}] {r['title']}\nURL: {r['url']}\nSnippet: {r['snippet']}"
                for idx, r in enumerate(results)
            )
            return [TextContent(type="text", text=formatted)]

        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as exc:
        # Return the error to the LLM, do not raise.
        return [TextContent(type="text", text=f"Web search tool error: {exc}")]


async def run_server() -> None:
    """Run the MCP server over stdio."""
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


async def run_self_test() -> None:
    """Run in-memory self-tests of the web search MCP handlers."""
    print("\n=== MCP web search server self-test ===")

    res = await call_tool("web_search", {"query": "model context protocol", "limit": 2})
    print(f"Search results:\n{res[0].text}\n")
    assert "modelcontextprotocol.io" in res[0].text

    res_lg = await call_tool("web_search", {"query": "LangGraph multi-agent", "limit": 1})
    print(f"LangGraph results:\n{res_lg[0].text}\n")
    assert "docs.langchain.com" in res_lg[0].text

    res_err = await call_tool("web_search", {"query": ""})
    print(f"Empty query handling: {res_err[0].text}")
    assert "Search error" in res_err[0].text

    print("\nAll web search MCP server tool tests passed.")


def main() -> None:
    """Serve over stdio when a client spawned us; self-test on a terminal."""
    if sys.stdin.isatty():
        anyio.run(run_self_test)
    else:
        anyio.run(run_server)


if __name__ == "__main__":
    main()
