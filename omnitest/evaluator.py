"""
evaluator.py
Evaluates LLM responses against rule-based checks defined in each test case.

Checks:
    1. Expected keywords exist (case-insensitive)
    2. Forbidden keywords are absent (case-insensitive)
    3. Response latency is within the allowed limit
"""

from typing import Dict, Any, List


def evaluate(test_case: Dict[str, Any], response: str,
             latency: float = 0.0) -> Dict[str, Any]:
    """
    Evaluate a single LLM response against the rules in a test case.

    Args:
        test_case: Test-case dict (must contain at least "id").
        response:  The LLM's response text.
        latency:   Measured response time in seconds.

    Returns:
        {
            "test_id": str,
            "pass": bool,
            "score": float,   # 0.0 – 1.0 (fraction of checks passed)
            "issues": [str],  # human-readable descriptions of failures
        }
    """
    total_checks = 0
    passed_checks = 0
    issues: List[str] = []

    # 1. Expected keywords ---------------------------------------------------
    expected_keywords: List[str] = test_case.get("expected_keywords", [])
    if expected_keywords:
        total_checks += 1
        found = [kw for kw in expected_keywords if kw.lower() in response.lower()]
        if found:
            passed_checks += 1
        else:
            issues.append(
                f"Missing expected keywords: none of {expected_keywords} found"
            )

    # 2. Forbidden keywords --------------------------------------------------
    forbidden_keywords: List[str] = test_case.get("forbidden_keywords", [])
    if forbidden_keywords:
        total_checks += 1
        found = [kw for kw in forbidden_keywords if kw.lower() in response.lower()]
        if not found:
            passed_checks += 1
        else:
            issues.append(
                f"Forbidden keywords detected: {found}"
            )

    # 3. Latency within limit ------------------------------------------------
    max_latency: float = test_case.get("max_latency", 0)
    if max_latency > 0:
        total_checks += 1
        if latency <= max_latency:
            passed_checks += 1
        else:
            issues.append(
                f"Latency {latency:.3f}s exceeded limit of {max_latency}s"
            )

    # --- Compute score ------------------------------------------------------
    score = passed_checks / total_checks if total_checks > 0 else 1.0
    passed = len(issues) == 0

    return {
        "test_id": test_case.get("id", "unknown"),
        "pass": passed,
        "score": round(score, 2),
        "issues": issues,
    }
