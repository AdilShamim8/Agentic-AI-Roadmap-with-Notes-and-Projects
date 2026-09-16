"""Tool discovery and registry demonstration for MCP and LangGraph agents.

Demonstrates:
1. Static registry schema storing tool servers, versions, and capabilities
2. Capability-based filtering (loading only relevant servers for a given task)
3. Semantic version constraints and compatibility checks
4. Registry query APIs and lifecycle management

Run:
    python examples/tool_registry_demo.py
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Set


SAMPLE_REGISTRY_DATA: Dict[str, List[Dict[str, Any]]] = {
    "servers": [
        {
            "name": "filesystem",
            "command": "python",
            "args": ["examples/mcp_filesystem_server.py"],
            "transport": "stdio",
            "capabilities": ["read_file", "list_directory"],
            "version": "1.0.0",
        },
        {
            "name": "web_search",
            "command": "python",
            "args": ["examples/mcp_websearch_server.py"],
            "transport": "stdio",
            "capabilities": ["web_search"],
            "version": "1.2.0",
        },
        {
            "name": "sqlite_db",
            "command": "python",
            "args": ["examples/mcp_sqlite_server.py"],
            "transport": "stdio",
            "capabilities": ["sql_query", "schema_discovery"],
            "version": "2.1.0",
        },
    ]
}


class ToolRegistry:
    """Registry managing available MCP tool servers and matching capabilities."""

    def __init__(self, registry_dict: Optional[Dict[str, Any]] = None) -> None:
        self.servers = (registry_dict or SAMPLE_REGISTRY_DATA).get("servers", [])

    def filter_by_capabilities(self, required_capabilities: List[str]) -> List[Dict[str, Any]]:
        """Find all servers matching at least one required capability."""
        needed = set(required_capabilities)
        matched_servers = []
        for server in self.servers:
            server_caps = set(server.get("capabilities", []))
            if needed & server_caps:
                matched_servers.append(server)
        return matched_servers

    def get_server_by_version(self, name: str, min_major_version: int) -> Optional[Dict[str, Any]]:
        """Retrieve server if it meets semantic major version constraints."""
        for server in self.servers:
            if server["name"] == name:
                ver_str = server.get("version", "1.0.0")
                major_ver = int(ver_str.split(".")[0])
                if major_ver >= min_major_version:
                    return server
                raise ValueError(
                    f"Version Mismatch: Server '{name}' version {ver_str} does not satisfy "
                    f"minimum major version requirement {min_major_version}.x"
                )
        return None

    def export_langgraph_config(self, matched_servers: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Export connection dictionary for MultiServerMCPClient."""
        config = {}
        for s in matched_servers:
            config[s["name"]] = {
                "command": s["command"],
                "args": s["args"],
                "transport": s["transport"],
            }
        return config


def main() -> None:
    """Run registry discovery and capability negotiation tests."""
    print("\n=== Tool Discovery and Registry Demo ===")
    registry = ToolRegistry()

    # Test 1: Capability matching for research agent (needs web_search and filesystem)
    print("Test 1: Resolving servers for research capabilities ['web_search', 'read_file']...")
    matched = registry.filter_by_capabilities(["web_search", "read_file"])
    matched_names = [s["name"] for s in matched]
    print(f"  Matched Servers: {matched_names}")
    assert "web_search" in matched_names
    assert "filesystem" in matched_names
    assert "sqlite_db" not in matched_names

    # Test 2: MultiServerMCPClient config generation
    print("\nTest 2: Exporting client connection manifest...")
    client_config = registry.export_langgraph_config(matched)
    print(f"  Generated Config: {json.dumps(client_config, indent=2)}")
    assert len(client_config) == 2

    # Test 3: Version constraint check (Valid)
    print("\nTest 3: Checking semantic version compatibility for 'sqlite_db' (min v2)...")
    server_v2 = registry.get_server_by_version("sqlite_db", min_major_version=2)
    assert server_v2 is not None
    print(f"  Verified: {server_v2['name']} is version {server_v2['version']}")

    # Test 4: Version constraint failure (Invalid)
    print("\nTest 4: Testing version constraint rejection (min v3 on v2 server)...")
    try:
        registry.get_server_by_version("sqlite_db", min_major_version=3)
        assert False, "Should have raised ValueError on version mismatch"
    except ValueError as exc:
        print(f"  Caught expected error: {exc}")

    print("\nAll registry discovery and capability negotiation assertions passed.")


if __name__ == "__main__":
    main()
