"""MCP Web Search server.

Exposes tools over the Model Context Protocol for web search:
- web_search: retrieves curated search results with snippets, URLs, and titles

Run:
    python examples/mcp_websearch_server.py
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

try:
    import anyio
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool
    HAS_MCP_SDK = True
except ImportError:
    HAS_MCP_SDK = False

    class TextContent:  # type: ignore[no-redef]
        def __init__(self, type: str, text: str) -> None:
            self.type = type
            self.text = text

    class Tool:  # type: ignore[no-redef]
        def __init__(self, name: str, description: str, inputSchema: dict) -> None:
            self.name = name
            self.description = description
            self.inputSchema = inputSchema

    class Server:  # type: ignore[no-redef]
        def __init__(self, name: str) -> None:
            self.name = name
            self._list_tools_handler: Optional[Any] = None
            self._call_tool_handler: Optional[Any] = None

        def list_tools(self) -> Any:
            def dec(fn: Any) -> Any:
                self._list_tools_handler = fn
                return fn
            return dec

        def call_tool(self) -> Any:
            def dec(fn: Any) -> Any:
                self._call_tool_handler = fn
                return fn
            return dec


server = Server("websearch-server")

# Curated reference index for deterministic evaluation and testing
KNOWLEDGE_INDEX = [
    {
        "title": "Model Context Protocol (MCP) Specification",
        "url": "https://modelcontextprotocol.io/introduction",
        "snippet": "An open standard for connecting AI assistants to data sources, tools, and developmental environments.",
        "keywords": ["mcp", "model context protocol", "tools", "specification"],
    },
    {
        "title": "LangGraph: Orchestrating Complex Agent Workflows",
        "url": "https://langchain-ai.github.io/langgraph/",
        "snippet": "A library for building stateful, multi-actor applications with LLMs, featuring cycle support, persistence, and human-in-the-loop.",
        "keywords": ["langgraph", "agents", "state", "orchestration", "multi-agent"],
    },
    {
        "title": "Agent-to-Agent (A2A) Protocol Standard",
        "url": "https://a2a-standard.org/overview",
        "snippet": "Standardized communication patterns for autonomous agent handoffs, collaborative swarm negotiation, and task delegation.",
        "keywords": ["a2a", "handoff", "interop", "multi-agent"],
    },
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List tools exposed by Web Search MCP server."""
    return [
        Tool(
            name="web_search",
            description=(
                "Search the web for technical documentation, research papers, and developer ecosystem guides. "
                "Returns titles, URLs, and text snippets."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query keywords"},
                    "limit": {"type": "integer", "description": "Maximum number of results to return (default: 3)"},
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
            limit = arguments.get("limit", 3)

            if not query.strip():
                return [TextContent(type="text", text="Search Error: Query string cannot be empty.")]

            query_terms = query.split()
            matched = []

            for item in KNOWLEDGE_INDEX:
                score = sum(1 for term in query_terms if term in item["title"].lower() or any(term in kw for kw in item["keywords"]))
                if score > 0:
                    matched.append((score, item))

            matched.sort(key=lambda x: x[0], reverse=True)
            results = [item for _, item in matched[:limit]]

            if not results:
                # Fallback to general top items if specific match not found
                results = KNOWLEDGE_INDEX[:limit]

            formatted = "\n\n".join(
                f"[{idx+1}] {r['title']}\nURL: {r['url']}\nSnippet: {r['snippet']}"
                for idx, r in enumerate(results)
            )
            return [TextContent(type="text", text=formatted)]

        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as exc:
        return [TextContent(type="text", text=f"Web Search Tool Error: {exc}")]


def run_standalone_test() -> None:
    """Run in-memory self-test of Web Search MCP handlers."""
    print("\n=== MCP Web Search Server Self-Test ===")
    import asyncio

    async def _test() -> None:
        # Test 1: Query MCP documentation
        res = await call_tool("web_search", {"query": "model context protocol", "limit": 2})
        print(f"Search Results:\n{res[0].text}\n")
        assert "modelcontextprotocol.io" in res[0].text

        # Test 2: Query LangGraph orchestration
        res_lg = await call_tool("web_search", {"query": "LangGraph multi-agent", "limit": 1})
        print(f"LangGraph Results:\n{res_lg[0].text}\n")
        assert "langchain-ai.github.io" in res_lg[0].text

        # Test 3: Empty query error handling
        res_err = await call_tool("web_search", {"query": ""})
        print(f"Empty query handling:\n{res_err[0].text}")
        assert "Search Error" in res_err[0].text

    asyncio.run(_test())
    print("\nAll Web Search MCP server tool tests passed successfully.")


if __name__ == "__main__":
    if HAS_MCP_SDK:
        try:
            async def main() -> None:
                async with stdio_server() as (read, write):
                    await server.run(read, write, server.create_initialization_options())
            anyio.run(main)
        except Exception:
            run_standalone_test()
    else:
        run_standalone_test()
