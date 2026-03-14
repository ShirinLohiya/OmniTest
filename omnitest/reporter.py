"""
reporter.py
Generates a summary report of test results.

Metrics:
    - Total tests
    - Passed / Failed counts and pass rate
    - Average latency
    - Failure breakdown (per-test issues)
"""

from typing import List, Dict, Any
from collections import defaultdict


def generate_report(results: List[Dict[str, Any]]) -> str:
    """
    Build and print a formatted summary report.

    Args:
        results: List of result dicts from the runner, each containing
                 at minimum: id, pass, latency, issues.

    Returns:
        The full report as a string (also printed to stdout).
    """
    total = len(results)
    passed = sum(1 for r in results if r["pass"])
    failed = total - passed
    pass_rate = (passed / total * 100) if total else 0
    avg_latency = (
        sum(r.get("latency", 0) for r in results) / total if total else 0
    )

    # ── Build report ──────────────────────────────────────────────────────
    lines: List[str] = []
    lines.append("")
    lines.append("OmniTest Report")
    lines.append("─" * 40)
    lines.append(f"Total tests     : {total}")
    lines.append(f"Passed          : {passed}")
    lines.append(f"Failed          : {failed}")
    lines.append(f"Pass rate       : {pass_rate:.1f}%")
    lines.append(f"Average latency : {avg_latency:.2f}s")

    # ── Per-test results ──────────────────────────────────────────────────
    lines.append("")
    lines.append("Results")
    lines.append("─" * 40)

    for r in results:
        icon = "✅" if r["pass"] else "❌"
        score_pct = r.get("score", 0) * 100
        lines.append(f"  {icon} {r['id']}  (score: {score_pct:.0f}%)")

    # ── Failure breakdown ─────────────────────────────────────────────────
    failures = [r for r in results if not r["pass"]]
    if failures:
        lines.append("")
        lines.append("Failure Breakdown")
        lines.append("─" * 40)
        for r in failures:
            lines.append(f"  ❌ {r['id']}")
            lines.append(f"       Prompt : {r.get('prompt', 'N/A')[:70]}")
            for issue in r.get("issues", []):
                lines.append(f"       • {issue}")

    lines.append("")
    lines.append("─" * 40)
    lines.append("")

    report = "\n".join(lines)
    print(report)
    return report
