"""Governance demonstration: permissions, audit log, PII redaction.

Implements chapter 08/06:
1. Permissioned tools (RBAC; the tool checks the role again inside the
   tool - defense in depth)
2. An append-only audit log of every call
3. PII redaction at the boundary, before anything is logged

Deterministic and keyless.

Run:
    python examples/governance_demo.py
"""

from __future__ import annotations

import json
import tempfile
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AUDIT_LOG = Path(tempfile.gettempdir()) / "governance_audit.jsonl"

PII_FIELDS = {"order_id", "email", "ssn"}


def redact(args: dict[str, Any]) -> dict[str, Any]:
    """Redact PII before it reaches logs or traces."""
    return {k: ("[REDACTED]" if k in PII_FIELDS else v) for k, v in args.items()}


def audit(event: dict[str, Any]) -> None:
    """Append-only audit log: one JSON line per event, never rewritten."""
    with AUDIT_LOG.open("a") as fh:
        fh.write(json.dumps(event) + "\n")


def governed_tool(
    tool_func: Callable[..., str], required_role: str
) -> Callable[..., str]:
    """Wrap a tool with a permission check, PII redaction, and audit."""

    def wrapper(user_id: str, user_role: str, **kwargs: Any) -> str:
        ts = datetime.now(timezone.utc).isoformat()
        if user_role != required_role:
            audit({
                "event": "permission_denied", "user": user_id,
                "tool": tool_func.__name__, "required_role": required_role,
                "user_role": user_role, "timestamp": ts,
            })
            return f"Permission denied. Requires role: {required_role}."

        result = tool_func(**kwargs)
        audit({
            "event": "tool_call", "user": user_id, "tool": tool_func.__name__,
            "args": redact(kwargs), "success": True, "timestamp": ts,
        })
        return result

    return wrapper


def _issue_refund_impl(order_id: str, amount: float) -> str:
    return f"refund of ${amount:.2f} issued for {order_id}"


issue_refund = governed_tool(_issue_refund_impl, required_role="admin")


def main() -> None:
    """Exercise allow, deny, and PII redaction paths."""
    print("\n=== Governance demo ===\n")
    AUDIT_LOG.write_text("")  # fresh log for this run

    allowed = issue_refund(
        user_id="alice", user_role="admin",
        order_id="ACME-123", amount=75.0,
    )
    print(f"1. admin call:    {allowed}")

    denied = issue_refund(
        user_id="bob", user_role="user",
        order_id="ACME-456", amount=25.0,
    )
    print(f"2. regular user:  {denied}")

    events = [json.loads(line) for line in AUDIT_LOG.read_text().splitlines() if line]
    print(f"\nAudit log ({len(events)} events, append-only at {AUDIT_LOG}):")
    for e in events:
        print(f"  {e['event']}: {e['tool']} args={e.get('args', {})}")

    assert any(e["event"] == "permission_denied" for e in events)
    tool_calls = [e for e in events if e["event"] == "tool_call"]
    assert tool_calls, "No successful call was audited"
    assert tool_calls[0]["args"]["order_id"] == "[REDACTED]", \
        "PII must be redacted before logging"
    assert "ACME-123" not in json.dumps(events), "Raw PII leaked into the audit log"

    print("\nGovernance checks passed (RBAC, audit, PII redaction).")


if __name__ == "__main__":
    main()
