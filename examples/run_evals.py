"""Eval runner for the agentic AI roadmap examples.

Runs the golden dataset (datasets/support_eval_30rows.csv) through a
tool-selection classifier and scores intent and tool accuracy against
the labeled expectations, compares to a baseline, writes a Markdown
report, and exits non-zero on regression (the CI gate). Deterministic
and keyless, so CI runs without secrets.

Used by `make eval` and by the CI workflow
(.github/workflows/eval-regression.yml).

Run:
    python examples/run_evals.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / "datasets" / "support_eval_30rows.csv"
BASELINE_PATH = Path(__file__).resolve().parent / "eval_baseline.json"
REPORT_PATH = ROOT / "eval_report.md"

REFUND_WORDS = ("refund", "money back", "charged", "billed", "billing", "duplicate charge")
BUG_WORDS = ("crash", "error", "500", "broken", "traceback", "bug", "failing", "not working")
INJECTION_WORDS = ("ignore previous instructions", "disregard your instructions",
                   "reveal the system prompt")
CANCEL_WORDS = ("cancel", "subscription")
ORDER_STATUS_WORDS = ("status", "where is my order", "track my", "shipped yet")
FEATURE_WORDS = ("add ", "support for", "will you ever", "calendar view", "dark mode",
                 "csv", "keyboard shortcuts", "api for developers")

INTENT_TO_TOOL = {
    "refund": "issue_refund",
    "bug": "escalate_to_human",
    "injection": "escalate_to_human",
    "cancel": "cancel_order",
    "order_status": "get_order_status",
    "feature_request": "search_docs",
    "question": "search_docs",
}


def load_dataset() -> list[dict[str, Any]]:
    """Load the golden dataset (30 labeled rows)."""
    with DATASET_PATH.open() as fh:
        return list(csv.DictReader(fh))


def classify_intent(message: str) -> str:
    """Keyword classifier (deterministic; a cheap LLM call in production)."""
    lowered = message.lower()
    if any(w in lowered for w in INJECTION_WORDS):
        return "injection"
    if any(w in lowered for w in REFUND_WORDS):
        return "refund"
    if any(w in lowered for w in BUG_WORDS):
        return "bug"
    if any(w in lowered for w in CANCEL_WORDS):
        return "cancel"
    if any(w in lowered for w in ORDER_STATUS_WORDS):
        return "order_status"
    if any(w in lowered for w in FEATURE_WORDS):
        return "feature_request"
    return "question"


def load_baseline() -> dict:
    """Load the baseline eval scores."""
    if not BASELINE_PATH.exists():
        return {"intent_accuracy": 0.0, "tool_accuracy": 0.0}
    return json.loads(BASELINE_PATH.read_text())


def run_eval() -> dict:
    """Run the eval suite and return the scores."""
    rows = load_dataset()
    correct_intent = 0
    correct_tool = 0
    for row in rows:
        predicted_intent = classify_intent(row["input"])
        predicted_tool = INTENT_TO_TOOL[predicted_intent]
        correct_intent += predicted_intent == row["expected_intent"]
        correct_tool += predicted_tool == row["expected_tool"]

    n = len(rows)
    return {
        "intent_accuracy": correct_intent / n,
        "tool_accuracy": correct_tool / n,
        "rows": n,
    }


def write_report(current: dict, baseline: dict) -> bool:
    """Write the Markdown report. Returns True if the eval passed (no regression)."""
    lines = ["# Eval Report", ""]
    lines.append("| Metric | Baseline | Current | Delta | Status |")
    lines.append("|--------|----------|---------|-------|--------|")

    passed = True
    for key in ("intent_accuracy", "tool_accuracy"):
        baseline_val = baseline.get(key, 0.0)
        current_val = current[key]
        delta = current_val - baseline_val
        # Regression threshold: a drop of more than 2 percentage points.
        status = "PASS" if delta >= -0.02 else "REGRESSION"
        if status == "REGRESSION":
            passed = False
        lines.append(
            f"| {key} | {baseline_val:.3f} | {current_val:.3f} | {delta:+.3f} | {status} |"
        )

    lines.append("")
    lines.append(f"Rows: {current.get('rows', 'N/A')}")
    REPORT_PATH.write_text("\n".join(lines) + "\n")
    print(f"[+] Report written to {REPORT_PATH}")
    return passed


def main() -> None:
    """Run the eval and exit non-zero on regression."""
    print("[+] Running eval...")
    current = run_eval()
    baseline = load_baseline()
    print(f"[+] Current scores: {current}")
    print(f"[+] Baseline scores: {baseline}")

    passed = write_report(current, baseline)
    if passed:
        print("[+] Eval passed.")
        sys.exit(0)
    print("[!] Eval regressed. Blocking merge.")
    sys.exit(1)


if __name__ == "__main__":
    main()
