"""MCP SQLite Database server.

Exposes tools over the Model Context Protocol for interacting with SQLite:
- query_database: executes read-only SQL queries and returns formatted rows
- list_tables: discovers available table names in the database
- describe_table: inspects column names and types for a specific table

Run:
    python examples/mcp_sqlite_server.py
"""

from __future__ import annotations

import json
import sqlite3
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


server = Server("sqlite-server")

# In-memory database initialization with sample schema and seed records
def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE models (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            provider TEXT NOT NULL,
            context_window INTEGER,
            cost_per_m_input REAL
        )
    """)
    cursor.executemany(
        "INSERT INTO models VALUES (?, ?, ?, ?, ?)",
        [
            (1, "claude-3-5-sonnet", "anthropic", 200000, 3.0),
            (2, "gpt-4o", "openai", 128000, 2.5),
            (3, "gemini-1-5-pro", "google", 2000000, 1.25),
        ],
    )
    conn.commit()
    return conn


SHARED_CONN = get_db_connection()


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List tools exposed by SQLite MCP server."""
    return [
        Tool(
            name="query_database",
            description=(
                "Execute a read-only SQL query against the database. "
                "Use for SELECT queries to fetch metrics, records, or aggregates. "
                "Destructive operations (DROP, DELETE, UPDATE) are blocked."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string", "description": "SQL query to execute, e.g. 'SELECT * FROM models'"}
                },
                "required": ["sql"],
            },
        ),
        Tool(
            name="list_tables",
            description="List all tables present in the database.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="describe_table",
            description="Get the column schema and datatypes for a specified table name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Name of the table to inspect"}
                },
                "required": ["table_name"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute SQLite operations safely and return text content."""
    try:
        cursor = SHARED_CONN.cursor()

        if name == "list_tables":
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = [row[0] for row in cursor.fetchall()]
            return [TextContent(type="text", text=json.dumps(tables, indent=2))]

        if name == "describe_table":
            table_name = arguments.get("table_name", "")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [{"column": row[1], "type": row[2], "notnull": bool(row[3])} for row in cursor.fetchall()]
            if not columns:
                return [TextContent(type="text", text=f"Table '{table_name}' does not exist.")]
            return [TextContent(type="text", text=json.dumps(columns, indent=2))]

        if name == "query_database":
            sql = arguments.get("sql", "").strip()
            # Guard against mutations
            if not sql.upper().startswith("SELECT") and not sql.upper().startswith("WITH") and not sql.upper().startswith("PRAGMA"):
                return [TextContent(type="text", text="Access Error: Only read-only queries (SELECT) are permitted.")]

            cursor.execute(sql)
            col_names = [d[0] for d in cursor.description] if cursor.description else []
            rows = [dict(zip(col_names, r)) for r in cursor.fetchall()]
            return [TextContent(type="text", text=json.dumps(rows, indent=2))]

        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as exc:
        return [TextContent(type="text", text=f"Database Query Error: {exc}")]


def run_standalone_test() -> None:
    """Run in-memory self-test of SQLite MCP handlers."""
    print("\n=== MCP SQLite Server Self-Test ===")
    import asyncio

    async def _test() -> None:
        # Test 1: List tables
        res_tables = await call_tool("list_tables", {})
        print(f"Tables Discovered: {res_tables[0].text}")
        assert "models" in res_tables[0].text

        # Test 2: Describe schema
        res_schema = await call_tool("describe_table", {"table_name": "models"})
        print(f"\nSchema for 'models':\n{res_schema[0].text}")
        assert "context_window" in res_schema[0].text

        # Test 3: Valid query
        res_query = await call_tool("query_database", {"sql": "SELECT name, provider, cost_per_m_input FROM models WHERE cost_per_m_input < 3.0"})
        print(f"\nQuery Results:\n{res_query[0].text}")
        assert "gemini-1-5-pro" in res_query[0].text

        # Test 4: Blocked destructive query
        res_drop = await call_tool("query_database", {"sql": "DROP TABLE models"})
        print(f"\nBlocked Query Result: {res_drop[0].text}")
        assert "Access Error" in res_drop[0].text

    asyncio.run(_test())
    print("\nAll SQLite MCP server tool tests passed successfully.")


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
