"""Tool design demonstration comparing anti-patterns with production-grade tools.

Demonstrates:
1. The 4 major tool design flaws:
   - Vague docstrings
   - Ambiguous parameter types
   - Silent error suppression
   - Overly broad monolithic tools
2. Production-grade tool contracts:
   - Positive usage conditions ("Use this when:")
   - Negative constraints ("Do NOT use this when:")
   - Format validation with actionable guidance
   - Informative, non-crashing error payloads

Run:
    python examples/tool_design_demo.py
"""

from __future__ import annotations

import re

from langchain_core.tools import tool


# --- Anti-Pattern: Poorly Designed Tool ---
@tool
def query(data: str) -> str:
    """Queries the system."""
    # Vague parameters, no validation, silent failure on malformed input
    if not data:
        return ""
    return f"Result for {data}"


# --- Production-Grade: Well-Designed Tool ---
@tool
def get_order_status(order_id: str) -> str:
    """Check the current status of a customer's order.

    Use this when:
    - The customer asks where their order is
    - The customer mentions a delayed, missing, or damaged order
    - You need to verify an order exists before processing a refund or return

    Do NOT use this when:
    - The customer is asking a general product question (use search_docs instead)
    - The customer wants to cancel an order (use cancel_order instead)
    - The customer wants to track a shipment carrier directly (use get_tracking_info instead)

    Args:
        order_id: The order identifier, format 'ACME-XXXXXX' (e.g., 'ACME-123456').
                  If the customer gives a different format, ask them to clarify
                  before calling this tool.

    Returns:
        A string describing the order status, or an informative message if not found.
    """
    pattern = r"^ACME-\d{6}$"
    if not re.match(pattern, order_id):
        return (
            f"Validation Error: '{order_id}' does not match expected format 'ACME-XXXXXX'. "
            f"Ask the user for their 6-digit order number prefixed with 'ACME-'."
        )

    # Simulated database lookup
    mock_db: dict[str, dict[str, str]] = {
        "ACME-100001": {"status": "shipped", "date": "2026-09-10", "tracking": "TRK-982341"},
        "ACME-100002": {"status": "processing", "date": "2026-09-15", "tracking": "Pending"},
    }

    if order_id in mock_db:
        record = mock_db[order_id]
        return (
            f"Order {order_id}: {record['status']} on {record['date']}, "
            f"tracking {record['tracking']}"
        )

    return f"Order {order_id} not found in database. Check the order ID and try again."


def main() -> None:
    """Evaluate tool behavior under edge cases and malformed inputs."""
    print("\n=== Tool Design Principles & Validation Demo ===")

    print("1. Testing poor tool anti-pattern:")
    poor_result = query.invoke({"data": ""})
    print(f"  Empty input output: {poor_result!r} (silent failure - zero guidance)")
    assert poor_result == ""

    print("\n2. Testing well-designed tool with valid input:")
    valid_result = get_order_status.invoke({"order_id": "ACME-100001"})
    print(f"  Result: {valid_result}")
    assert "shipped on 2026-09-10" in valid_result

    print("\n3. Testing well-designed tool with missing order ID:")
    not_found_result = get_order_status.invoke({"order_id": "ACME-999999"})
    print(f"  Result: {not_found_result}")
    assert "not found in database" in not_found_result

    print("\n4. Testing well-designed tool with invalid format:")
    invalid_format_result = get_order_status.invoke({"order_id": "12345"})
    print(f"  Result: {invalid_format_result}")
    assert "Validation Error" in invalid_format_result
    assert "ACME-XXXXXX" in invalid_format_result

    print("\nTool design validation assertions passed successfully.")


if __name__ == "__main__":
    main()
