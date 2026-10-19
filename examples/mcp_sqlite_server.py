"""MCP SQLite database server.

Exposes tools over the Model Context Protocol for interacting with SQLite:
- query_database: executes read-only SQL queries and returns formatted rows
- list_tables: discovers available table names in the database
- describe_table: inspects column names and types for a specific table

Run:
    python examples/mcp_sqlite_server.py

With a terminal stdin (no MCP client attached) this runs a self-test;
with a piped stdin (an MCP client spawned us) it speaks JSON-RPC.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from typing import Any

import anyio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

server = Server("sqlite-server")


def get_db_connection() -> sqlite3.Connection:
    """Create the in-memory demo database with sample schema and rows.

    The model names and prices are illustrative sample data for the demo
    database, not a pricing reference.
    """
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
            (1, "claude-sonnet-5-5", "anthropic", 200000, 3.0),
            (2, "gpt-5.5", "openai", 400000, 1.25),
            (3, "gemini-4-argon", "google", 1000000, 1.25),
        ],
    )
    conn.commit()
    return conn


SHARED_CONN = get_db_connection()


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List the tools this server exposes."""
    return [
        Tool(
            name="query_database",
            description=(
                "Execute a read-only SQL query against the database. "
                "Use for SELECT queries to fetch metrics, records, or "
                "aggregates. Destructive operations are blocked."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "SQL query to execute, e.g. 'SELECT * FROM models'",
                    }
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
            description="Get the column schema and datatypes for a table.",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table to inspect",
                    }
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
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            tables = [row[0] for row in cursor.fetchall()]
            return [TextContent(type="text", text=json.dumps(tables, indent=2))]

        if name == "describe_table":
            table_name = arguments.get("table_name", "")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [
                {"column": row[1], "type": row[2], "notnull": bool(row[3])}
                for row in cursor.fetchall()
            ]
            if not columns:
                return [TextContent(type="text", text=f"Table '{table_name}' does not exist.")]
            return [TextContent(type="text", text=json.dumps(columns, indent=2))]

        if name == "query_database":
            sql = arguments.get("sql", "").strip()
            allowed_prefixes = ("SELECT", "WITH", "PRAGMA")
            if not sql.upper().startswith(allowed_prefixes):
                return [
                    TextContent(
                        type="text",
                        text="Access error: only read-only queries (SELECT) are permitted.",
                    )
                ]
            cursor.execute(sql)
            col_names = [d[0] for d in cursor.description] if cursor.description else []
            rows = [dict(zip(col_names, r, strict=False)) for r in cursor.fetchall()]
            return [TextContent(type="text", text=json.dumps(rows, indent=2))]

        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as exc:
        # Return the error to the LLM, do not raise.
        return [TextContent(type="text", text=f"Database query error: {exc}")]


async def run_server() -> None:
    """Run the MCP server over stdio."""
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


async def run_self_test() -> None:
    """Run in-memory self-tests of the SQLite MCP handlers."""
    print("\n=== MCP SQLite server self-test ===")

    res_tables = await call_tool("list_tables", {})
    print(f"Tables discovered: {res_tables[0].text}")
    assert "models" in res_tables[0].text

    res_schema = await call_tool("describe_table", {"table_name": "models"})
    print(f"\nSchema for 'models':\n{res_schema[0].text}")
    assert "context_window" in res_schema[0].text

    res_query = await call_tool(
        "query_database",
        {"sql": "SELECT name, provider FROM models WHERE cost_per_m_input < 2.0"},
    )
    print(f"\nQuery results:\n{res_query[0].text}")
    assert "gemini-4-argon" in res_query[0].text

    res_drop = await call_tool("query_database", {"sql": "DROP TABLE models"})
    print(f"\nBlocked query result: {res_drop[0].text}")
    assert "Access error" in res_drop[0].text

    print("\nAll SQLite MCP server tool tests passed.")


def main() -> None:
    """Serve over stdio when a client spawned us; self-test on a terminal."""
    if sys.stdin.isatty():
        anyio.run(run_self_test)
    else:
        anyio.run(run_server)


if __name__ == "__main__":
    main()
