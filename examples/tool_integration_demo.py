"""Tool integration demonstration with role-based access control and error handling.

Demonstrates:
1. Custom tools with typed arguments and docstrings
2. Graceful exception handling (returning descriptive error messages instead of crashing)
3. Dynamic tool scoping based on caller role (User vs Admin)
4. Tool execution logging (timing, arguments, return payload)

Run:
    python examples/tool_integration_demo.py
"""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional

try:
    from langchain_core.tools import tool
    HAS_LANGCHAIN_CORE = True
except ImportError:
    HAS_LANGCHAIN_CORE = False

    def tool(fn: Callable[..., Any]) -> Callable[..., Any]:  # type: ignore[no-redef]
        """Lightweight decorator preserving docstring and metadata."""
        fn.name = fn.__name__  # type: ignore[attr-defined]
        return fn


@tool
def get_order_status(order_id: str) -> str:
    """Get the status of an order. Available to all authenticated users."""
    valid_orders = {
        "ORD-101": "Shipped - In Transit",
        "ORD-102": "Delivered",
        "ORD-103": "Processing at Warehouse",
    }
    # Simulate network call with boundary validation
    if not order_id.startswith("ORD-"):
        return f"Tool Error: Invalid order format '{order_id}'. Order IDs must start with 'ORD-'."
    if order_id in valid_orders:
        return f"Order {order_id} status: {valid_orders[order_id]}"
    return f"Tool Notice: Order {order_id} not found in database. Please verify with customer."


@tool
def issue_refund(order_id: str, amount: float) -> str:
    """Issue a financial refund for an order. Restricted to Admin role only."""
    if amount <= 0:
        return f"Tool Error: Refund amount ${amount:.2f} must be greater than zero."
    if amount > 5000.0:
        return f"Tool Error: Refund amount ${amount:.2f} exceeds single-transaction limit of $5,000.00."
    return f"Success: Refund of ${amount:.2f} processed for order {order_id}. Reference #REF-{order_id[4:]}."


class ToolRegistry:
    """Manages role-based tool visibility and logged execution."""

    def __init__(self) -> None:
        self.call_logs: List[Dict[str, Any]] = []

    def get_tools_for_role(self, role: str) -> List[Callable[..., Any]]:
        """Return available tool set based on user role."""
        tools = [get_order_status]
        if role == "admin":
            tools.append(issue_refund)
        return tools

    def invoke_tool(self, tool_fn: Callable[..., Any], caller_role: str, **kwargs: Any) -> str:
        """Safely invoke tool with telemetry and access enforcement."""
        start = time.time()
        tool_name = getattr(tool_fn, "name", tool_fn.__name__)
        available_tools = [getattr(t, "name", t.__name__) for t in self.get_tools_for_role(caller_role)]

        if tool_name not in available_tools:
            result = f"Access Denied: Role '{caller_role}' is not authorized to invoke '{tool_name}'."
            self.call_logs.append({
                "tool": tool_name,
                "role": caller_role,
                "authorized": False,
                "latency": time.time() - start,
            })
            return result

        try:
            result = tool_fn(**kwargs)
        except Exception as exc:
            # Shield graph from crashing; return formatted error
            result = f"Unexpected Tool Execution Error: {exc}"

        elapsed = time.time() - start
        self.call_logs.append({
            "tool": tool_name,
            "role": caller_role,
            "args": kwargs,
            "result": result,
            "latency": elapsed,
            "authorized": True,
        })
        return result


def main() -> None:
    """Run verification of role permissions and error isolation."""
    print("\n=== LangGraph Tool Integration and Scoping Demo ===")
    registry = ToolRegistry()

    # Case 1: Standard user queries order status
    print("Case 1: Standard user queries valid order...")
    res1 = registry.invoke_tool(get_order_status, caller_role="user", order_id="ORD-101")
    print(f"  Result: {res1}")
    assert "Shipped" in res1

    # Case 2: Standard user tries to issue a refund (Permission Denied)
    print("\nCase 2: Standard user attempts administrative refund...")
    res2 = registry.invoke_tool(issue_refund, caller_role="user", order_id="ORD-101", amount=49.99)
    print(f"  Result: {res2}")
    assert "Access Denied" in res2

    # Case 3: Admin issues refund successfully
    print("\nCase 3: Administrator issues legitimate refund...")
    res3 = registry.invoke_tool(issue_refund, caller_role="admin", order_id="ORD-101", amount=49.99)
    print(f"  Result: {res3}")
    assert "Success: Refund" in res3

    # Case 4: Faulty argument handled gracefully without exception
    print("\nCase 4: Faulty input handled gracefully...")
    res4 = registry.invoke_tool(get_order_status, caller_role="user", order_id="invalid_123")
    print(f"  Result: {res4}")
    assert "Tool Error" in res4

    print(f"\nTotal Telemetry Records Logged: {len(registry.call_logs)}")
    assert len(registry.call_logs) == 4
    print("All tool integration and role-scoping tests passed successfully.")


if __name__ == "__main__":
    main()
